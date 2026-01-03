import math
from typing import Tuple
from dataclasses import dataclass


class MoveStatus:
    OK = "MOVE_OK"
    BARRIER = "HIT_BARRIER"
    BLOCKED = "MOVE_BLOCKED"


class SetStateStatus:
    OK = "STATE_OK"
    NO_WATER = "OUT_OF_WATER"
    NO_SOAP = "OUT_OF_SOAP"


@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    mode: int
    water: float
    soap: float


def create_robot():
    state = RobotState(0.0, 0.0, 0.0, 1, 50.0, 20.0)

    class RobotAPI:
        def move(self, distance: float) -> Tuple['RobotAPI', MoveStatus, str]:
            angle_rads = state.angle * (math.pi / 180.0)
            new_x = state.x + distance * math.cos(angle_rads)
            new_y = state.y + distance * math.sin(angle_rads)

            constrained_x = max(0, min(100, new_x))
            constrained_y = max(0, min(100, new_y))

            if new_x == constrained_x and new_y == constrained_y:
                state.x = new_x
                state.y = new_y
                return RobotAPI(), MoveStatus.OK, f"Moved to ({new_x:.1f}, {new_y:.1f})"
            else:
                state.x = constrained_x
                state.y = constrained_y
                return RobotAPI(), MoveStatus.BARRIER, f"Hit barrier at ({constrained_x:.1f}, {constrained_y:.1f})"

        def turn(self, angle: float) -> Tuple['RobotAPI', str, str]:
            state.angle = (state.angle + angle) % 360
            return RobotAPI(), "OK", f"Turned to {state.angle:.1f}°"

        def set_state(self, mode: int) -> Tuple['RobotAPI', SetStateStatus, str]:
            if mode == 1 and state.water <= 0:
                return RobotAPI(), SetStateStatus.NO_WATER, "No water"
            elif mode == 2 and state.soap <= 0:
                return RobotAPI(), SetStateStatus.NO_SOAP, "No soap"

            state.mode = mode
            if mode == 1:
                state.water -= 1.0
            elif mode == 2:
                state.soap -= 0.5

            return RobotAPI(), SetStateStatus.OK, f"Mode set to {mode}"

        def get_info(self) -> dict:
            return {
                "position": (state.x, state.y),
                "angle": state.angle,
                "mode": state.mode,
                "water": state.water,
                "soap": state.soap
            }

    return RobotAPI()


robot = create_robot()

robot, status, msg = robot.move(100)
print(f"Move: {msg} ({status})")

robot, status, msg = robot.move(50)
print(f"Move: {msg} ({status})")

robot, status, msg = robot.set_state(2)
print(f"Set state: {msg} ({status})")

for i in range(5):
    robot, status, msg = robot.set_state(1)
    print(f"Set water attempt {i + 1}: {msg} ({status})")
    if status != SetStateStatus.OK:
        break

info = robot.get_info()
print(f"\nFinal state: {info}")

