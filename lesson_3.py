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
        self.__angle = self.__angle * (math.pi / 180.0)
        self.__x += int(distance) * math.cos(self.__angle)
        self.__y += int(distance) * math.sin(self.__angle)
        print('POS(', self.__x, ',', self.__y, ')')

    def turn(self, angle):
        self.__angle += int(angle)
        print(f"ANGLE {self.__angle}")

    def set_cleaning_state(self, state):
        try:
            self.__cleaning_state = CleaningState(state)
            print(f"STATE {self.__cleaning_state}")
        except ValueError:
            print(f"Wrong cleaning state {state}, water, soap, brush are accesible")

    def start(self):
        print(f"START WITH {CleaningState(self.__cleaning_state)}")

    def stop(self):
        print("STOP")


def activate_cleaner_bot(cleanerBot: CleanerBot):
    return {
        'move': cleanerBot.move,
        'turn': cleanerBot.turn,
        'set': cleanerBot.set_cleaning_state,
        'start': cleanerBot.start,
        'stop': cleanerBot.stop
    }


bot = activate_cleaner_bot(CleanerBot())
running = True
while running:
    commands = input("Commands: ").split(',')
    for command in commands:
        command_name, _, param = command.strip().partition(' ')
        if command_name in ("exit", "quit", "q"):
            running = False
            break

        if command_name in bot:
            if command_name in ("stop", "start"):
                bot[command_name]()
            else:
                bot[command_name](param)
        else:
            print(f"Unknown command: {command_name}")
