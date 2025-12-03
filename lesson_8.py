import pure_robot

class CleanerBot:
    def __init__(self):
        self.__state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    def make(self, program):
        # передаём весь набор команд, а не одну строку
        self.__state = pure_robot.make(
            pure_robot.transfer_to_cleaner,
            program,
            self.__state
        )


bot = CleanerBot()

bot.make([
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
])