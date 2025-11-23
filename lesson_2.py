from enum import Enum
import math

class CleaningState(Enum):
    WATER = "water"
    SOAP = "soap"
    BRUSH = "brush"


cleaning_state = CleaningState.WATER
x = 0.0
y = 0.0
angle = 0


def move(distance):
    global angle, x, y
    angle_rads = angle * (math.pi / 180.0)
    x += int(distance) * math.cos(angle_rads)
    y += int(distance) * math.sin(angle_rads)
    print('POS(', x, ',', y, ')')


def turn(turn_angle):
    global angle
    angle += int(turn_angle)
    print(f"ANGLE {angle}")


def set_cleaning_state(state):
    global cleaning_state
    try:
        cleaning_state = CleaningState(state)
        print(f"STATE {state}")
    except ValueError:
        print(f"Wrong cleaning state {state}, water, soap, brush are accessible")


def start():
    print(f"START WITH {cleaning_state}")


def stop():
    print("STOP")


def get_cleaner_bot_commands():
    return {
        'move': move,
        'turn': turn,
        'set': set_cleaning_state,
        'start': start,
        'stop': stop
    }


commands_mapper = get_cleaner_bot_commands()

running = True
while running:
    commands = input("Commands: ").split(',')
    for command in commands:
        command_name, _, param = command.strip().partition(' ')
        if command_name in ("exit", "quit", "q"):
            running = False
            break

        if command_name in commands_mapper:
            if command_name in ("stop", "start"):
                commands_mapper[command_name]()
            else:
                commands_mapper[command_name](param)
        else:
            print(f"Unknown command: {command_name}")
