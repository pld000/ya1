# Stream Processing

import math
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Protocol


@dataclass
class RobotState:
    x: float
    y: float
    angle: float
    state: int


class CleaningMode(Enum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


class Event(ABC):
    @abstractmethod
    def apply(self, state: RobotState) -> RobotState:
        pass

    @abstractmethod
    def get_event_type(self) -> str:
        pass


@dataclass
class RobotMovedEvent(Event):
    distance: float

    def apply(self, state: RobotState) -> RobotState:
        r = state.angle * math.pi / 180.0
        return RobotState(
            state.x + self.distance * math.cos(r),
            state.y + self.distance * math.sin(r),
            state.angle,
            state.state
        )

    def get_event_type(self) -> str:
        return f"MOVED {self.distance}"


@dataclass
class RobotTurnedEvent(Event):
    angle: float

    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            state.x,
            state.y,
            state.angle + self.angle,
            state.state
        )

    def get_event_type(self) -> str:
        return f"TURNED {self.angle}"


@dataclass
class RobotStateChangedEvent(Event):
    new_state: CleaningMode

    def apply(self, state: RobotState) -> RobotState:
        return RobotState(
            state.x,
            state.y,
            state.angle,
            self.new_state.value
        )

    def get_event_type(self) -> str:
        return f"STATE {self.new_state.name}"


@dataclass
class RobotStartedEvent(Event):
    def apply(self, state: RobotState) -> RobotState:
        return state

    def get_event_type(self) -> str:
        return "STARTED"


@dataclass
class RobotStoppedEvent(Event):
    def apply(self, state: RobotState) -> RobotState:
        return state

    def get_event_type(self) -> str:
        return "STOPPED"


class Command(Protocol):
    def handle(self, state: RobotState) -> List[Event]:
        pass


@dataclass
class MoveCommand:
    distance: float

    def handle(self, state: RobotState) -> List[Event]:
        return [RobotMovedEvent(self.distance)]


@dataclass
class TurnCommand:
    angle: float

    def handle(self, state: RobotState) -> List[Event]:
        return [RobotTurnedEvent(self.angle)]


@dataclass
class SetStateCommand:
    state: CleaningMode

    def handle(self, state_: RobotState) -> List[Event]:
        return [RobotStateChangedEvent(self.state)]


@dataclass
class StartCommand:
    def handle(self, state: RobotState) -> List[Event]:
        return [RobotStartedEvent()]


@dataclass
class StopCommand:
    def handle(self, state: RobotState) -> List[Event]:
        return [RobotStoppedEvent()]


class EventBus:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, processor):
        self.subscribers.append(processor)

    def publish(self, events: List[Event]):
        for e in events:
            for s in self.subscribers:
                produced = s.process(e)
                if produced:
                    self.publish(produced)


class EventStore:
    def __init__(self, bus: EventBus):
        self.events: Dict[str, List[Event]] = {}
        self.bus = bus

    def append(self, robot_id: str, events: List[Event]):
        self.events.setdefault(robot_id, []).extend(events)
        self.bus.publish(events)

    def get(self, robot_id: str) -> List[Event]:
        return self.events.get(robot_id, [])


class StateProjector:
    def __init__(self, initial: RobotState):
        self.initial = initial

    def project(self, events: List[Event]) -> RobotState:
        s = self.initial
        for e in events:
            s = e.apply(s)
        return s


class CommandHandler:
    def __init__(self, store: EventStore, projector: StateProjector):
        self.store = store
        self.projector = projector

    def handle(self, robot_id: str, command: Command):
        state = self.projector.project(self.store.get(robot_id))
        events = command.handle(state)
        self.store.append(robot_id, events)


class LoggingProcessor:
    def process(self, event: Event):
        print(event.get_event_type())
        return []


class SafetyProcessor:
    def __init__(self):
        self.distance = 0

    def process(self, event: Event):
        if isinstance(event, RobotMovedEvent):
            self.distance += abs(event.distance)
            if self.distance > 120:
                return [RobotStoppedEvent()]
        return []


bus = EventBus()
bus.subscribe(LoggingProcessor())
bus.subscribe(SafetyProcessor())

store = EventStore(bus)
projector = StateProjector(RobotState(0, 0, 0, CleaningMode.WATER.value))
handler = CommandHandler(store, projector)

robot = "r1"

cmds = [
    MoveCommand(100),
    TurnCommand(-90),
    SetStateCommand(CleaningMode.SOAP),
    StartCommand(),
    MoveCommand(50),
    StopCommand()
]

for c in cmds:
    handler.handle(robot, c)

final_state = projector.project(store.get(robot))
print(final_state)
