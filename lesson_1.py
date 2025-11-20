from enum import Enum

class CleaningState(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"

class CleanerBot:
    def __init__(self):
        self.__cleaning_state = None

    def move(self, distance):
        print(f"POS {distance}")

    def turn(self, angle):
        print(f"ANGLE {angle}")

    def set_cleaning_state(self, state):
        try:
            self.__cleaning_state = CleaningState(state)
            print(f"STATE {state}")
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
