import math
from dataclasses import dataclass
from typing import Callable, Any
from enum import Enum
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3


class ResponseType(Enum):
    MOVE = "MOVE"
    TURN = "TURN"
    STATE = "STATE"
    START = "START"
    STOP = "STOP"


@dataclass
class MoveResponse:
    distance: float
    success: bool
    actual_distance: float


@dataclass
class TurnResponse:
    angle: float
    success: bool
    actual_angle: float


@dataclass
class StateResponse:
    new_state: int
    success: bool
    actual_state: int


@dataclass
class StartResponse:
    success: bool


@dataclass
class StopResponse:
    success: bool


class Command:
    def interpret(self, state: RobotState) -> tuple[Any, RobotState]:
        pass


@dataclass
class Move(Command):
    distance: float
    next: Callable[[MoveResponse], Command]

    def interpret(self, state: RobotState) -> tuple[MoveResponse, RobotState]:
        angle_rads = state.angle * (math.pi / 180.0)
        new_x = state.x + self.distance * math.cos(angle_rads)
        new_y = state.y + self.distance * math.sin(angle_rads)

        new_state = RobotState(new_x, new_y, state.angle, state.state)
        response = MoveResponse(
            distance=self.distance,
            success=True,
            actual_distance=self.distance
        )
        return response, new_state


@dataclass
class Turn(Command):
    angle: float
    next: Callable[[TurnResponse], Command]

    def interpret(self, state: RobotState) -> tuple[TurnResponse, RobotState]:
        new_angle = state.angle + self.angle
        new_state = RobotState(state.x, state.y, new_angle, state.state)
        response = TurnResponse(
            angle=self.angle,
            success=True,
            actual_angle=self.angle
        )
        return response, new_state


@dataclass
class SetState(Command):
    new_state: int
    next: Callable[[StateResponse], Command]

    def interpret(self, state: RobotState) -> tuple[StateResponse, RobotState]:
        new_state = RobotState(state.x, state.y, state.angle, self.new_state)
        response = StateResponse(
            new_state=self.new_state,
            success=True,
            actual_state=self.new_state
        )
        return response, new_state


@dataclass
class Start(Command):
    next: Callable[[StartResponse], Command]

    def interpret(self, state: RobotState) -> tuple[StartResponse, RobotState]:
        response = StartResponse(success=True)
        return response, state


@dataclass
class Stop(Command):
    def interpret(self, state: RobotState) -> tuple[StopResponse, RobotState]:
        response = StopResponse(success=True)
        return response, state


def interpret_ast(initial_state: RobotState, command: Command):
    current_state = initial_state
    current_command = command

    while not isinstance(current_command, Stop):
        response, new_state = current_command.interpret(current_state)
        current_state = new_state

        if isinstance(current_command, Move):
            current_command = current_command.next(response)
        elif isinstance(current_command, Turn):
            current_command = current_command.next(response)
        elif isinstance(current_command, SetState):
            current_command = current_command.next(response)
        elif isinstance(current_command, Start):
            current_command = current_command.next(response)

    final_response, final_state = current_command.interpret(current_state)
    return final_state


initial_state = RobotState(0.0, 0.0, 0, WATER)

program = Move(
    distance=100,
    next=lambda resp: Turn(
        angle=-90,
        next=lambda resp: SetState(
            new_state=SOAP,
            next=lambda resp: Start(
                next=lambda resp: Move(
                    distance=50,
                    next=lambda resp: Stop()
                )
            )
        )
    )
)

final_state = interpret_ast(initial_state, program)

print(f"Final state: {final_state}")