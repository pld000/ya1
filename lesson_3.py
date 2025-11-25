from enum import Enum
import math


class CleaningState(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"


class CleanerBot:
    def __init__(self):
        self.__cleaning_state = CleaningState.WATER
        self.__angle = 0
        self.__x = 0
        self.__y = 0

    def move(self, distance):
        angle_rads = self.__angle * (math.pi / 180.0)
        dist = float(distance)

        self.__x += dist * math.cos(angle_rads)
        self.__y += dist * math.sin(angle_rads)
        return f"POS ({self.__x}, {self.__y})"

    def turn(self, angle):
        self.__angle += float(angle)
        return f"ANGLE {self.__angle}"

    def set_cleaning_state(self, state):
        try:
            self.__cleaning_state = CleaningState(state)
            return f"STATE {state}"
        except ValueError:
            return f"Wrong cleaning state {state}, water, soap, brush are accessible"

    def start(self):
        return f"START WITH {self.__cleaning_state.value}"

    def stop(self):
        return "STOP"


def activate_cleaner_bot(cleaner: CleanerBot):
    return {
        "move": cleaner.move,
        "turn": cleaner.turn,
        "set": cleaner.set_cleaning_state,
        "start": cleaner.start,
        "stop": cleaner.stop,
    }


def transfer_to_cleaner(bot_command: str):
    mapper = activate_cleaner_bot(bot)
    name, _, params = bot_command.strip().partition(' ')
    if name not in mapper:
        return f"Unknown command: {name}"

    if params == '':
        return mapper[name]()
    else:
        return mapper[name](params)


bot = CleanerBot()

running = True
while running:
    commands = input("Commands: ").split(',')
    for command in commands:
        command = command.strip()
        if command in ("exit", "quit", "q"):
            running = False
            break

        result = transfer_to_cleaner(command)
        print(result)
