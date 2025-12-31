# Abstract Data Type

import math
from dataclasses import dataclass
from typing import Callable, Literal
from enum import IntEnum


class CleanerMode(IntEnum):
    WATER = 1
    SOAP = 2
    BRUSH = 3


@dataclass(frozen=True)
class CleanerState:
    _x: float
    _y: float
    _angle: float
    _mode: CleanerMode

    def __init__(self, x: float = 0.0, y: float = 0.0,
                 angle: float = 0.0, mode: CleanerMode = CleanerMode.WATER):
        object.__setattr__(self, '_x', x)
        object.__setattr__(self, '_y', y)
        object.__setattr__(self, '_angle', angle)
        object.__setattr__(self, '_mode', mode)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def angle(self) -> float:
        return self._angle

    @property
    def mode(self) -> CleanerMode:
        return self._mode

    def with_position(self, x: float, y: float) -> 'CleanerState':
        return CleanerState(x, y, self._angle, self._mode)

    def with_angle(self, angle: float) -> 'CleanerState':
        return CleanerState(self._x, self._y, angle, self._mode)

    def with_mode(self, mode: CleanerMode) -> 'CleanerState':
        return CleanerState(self._x, self._y, self._angle, mode)


class Cleaner:
    def __init__(self, transfer: Callable, initial_state: CleanerState = None):
        self._transfer = transfer
        self._state = initial_state or CleanerState()

    @property
    def state(self) -> CleanerState:
        return self._state

    def move(self, dist: float) -> 'Cleaner':
        angle_rads = self._state.angle * (math.pi / 180.0)
        new_x = self._state.x + dist * math.cos(angle_rads)
        new_y = self._state.y + dist * math.sin(angle_rads)

        new_state = self._state.with_position(new_x, new_y)
        self._transfer(('POS(', new_state.x, ',', new_state.y, ')'))

        return Cleaner(self._transfer, new_state)

    def turn(self, turn_angle: float) -> 'Cleaner':
        new_angle = self._state.angle + turn_angle
        new_state = self._state.with_angle(new_angle)

        self._transfer(('ANGLE', new_state.angle))
        return Cleaner(self._transfer, new_state)

    def set_mode(self, mode_name: Literal['water', 'soap', 'brush']) -> 'Cleaner':
        mode_map = {
            'water': CleanerMode.WATER,
            'soap': CleanerMode.SOAP,
            'brush': CleanerMode.BRUSH
        }

        if mode_name not in mode_map:
            return self

        new_state = self._state.with_mode(mode_map[mode_name])
        self._transfer(('STATE', new_state.mode))

        return Cleaner(self._transfer, new_state)

    def start(self) -> 'Cleaner':
        self._transfer(('START WITH', self._state.mode))
        return Cleaner(self._transfer, self._state)

    def stop(self) -> 'Cleaner':
        self._transfer(('STOP',))
        return Cleaner(self._transfer, self._state)

    def execute(self, commands: list[str]) -> 'Cleaner':
        cleaner = self

        for command in commands:
            parts = command.split(' ')
            cmd_name = parts[0]

            if cmd_name == 'move':
                cleaner = cleaner.move(int(parts[1]))
            elif cmd_name == 'turn':
                cleaner = cleaner.turn(int(parts[1]))
            elif cmd_name == 'set':
                cleaner = cleaner.set_mode(parts[1])
            elif cmd_name == 'start':
                cleaner = cleaner.start()
            elif cmd_name == 'stop':
                cleaner = cleaner.stop()

        return cleaner


def transfer_to_cleaner(message):
    print(message)


robot = Cleaner(transfer_to_cleaner)

final_robot = (robot
               .set_mode('soap')
               .start()
               .move(100)
               .turn(90)
               .move(50)
               .stop())