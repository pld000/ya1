# robot_interface.py
def transfer_to_cleaner(message):
    print(message)


# cleaner.py
import math


class Cleaner:
    WATER = 1
    SOAP = 2
    BRUSH = 3

    def __init__(self, transfer):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0
        self.state = self.WATER
        self.transfer = transfer

    def move(self, dist):
        angle_rads = self.angle * (math.pi / 180.0)
        self.x += dist * math.cos(angle_rads)
        self.y += dist * math.sin(angle_rads)
        self.transfer(('POS(', self.x, ',', self.y, ')'))

    def turn(self, turn_angle):
        self.angle += turn_angle
        self.transfer(('ANGLE', self.angle))

    def set_state(self, new_state):
        if new_state == 'water':
            self.state = self.WATER
        elif new_state == 'soap':
            self.state = self.SOAP
        elif new_state == 'brush':
            self.state = self.BRUSH
        self.transfer(('STATE', self.state))

    def start(self):
        self.transfer(('START WITH', self.state))

    def stop(self):
        self.transfer(('STOP',))

    def make(self, code):
        for command in code:
            cmd = command.split(' ')
            if cmd[0] == 'move':
                self.move(int(cmd[1]))
            elif cmd[0] == 'turn':
                self.turn(int(cmd[1]))
            elif cmd[0] == 'set':
                self.set_state(cmd[1])
            elif cmd[0] == 'start':
                self.start()
            elif cmd[0] == 'stop':
                self.stop()


# main.py
from robot_interface import transfer_to_cleaner
from cleaner import Cleaner


def main():
    cleaner = Cleaner(transfer_to_cleaner)
    cleaner.make((
        'move 100',
        'turn -90',
        'set soap',
        'start',
        'move 50',
        'stop'
    ))
