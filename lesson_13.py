import pure_robot


class Command:
    def execute(self, state):
        pass


class MoveCommand(Command):
    def __init__(self, distance):
        self.distance = distance

    def execute(self, state):
        return pure_robot.move(pure_robot.transfer_to_cleaner, self.distance, state)


class TurnCommand(Command):
    def __init__(self, angle):
        self.angle = angle

    def execute(self, state):
        return pure_robot.turn(pure_robot.transfer_to_cleaner, self.angle, state)


class SetCommand(Command):
    def __init__(self, mode):
        self.mode = mode

    def execute(self, state):
        return pure_robot.set_state(pure_robot.transfer_to_cleaner, self.mode, state)


class StartCommand(Command):
    def execute(self, state):
        return pure_robot.start(pure_robot.transfer_to_cleaner, state)


class StopCommand(Command):
    def execute(self, state):
        return pure_robot.stop(pure_robot.transfer_to_cleaner, state)


def execute_commands(commands, initial_state):
    state = initial_state
    for command in commands:
        state = command.execute(state)
    return state


commands = [
    MoveCommand(100),
    TurnCommand(-90),
    SetCommand('soap'),
    StartCommand(),
    MoveCommand(50),
    StopCommand()
]

initial_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
final_state = execute_commands(commands, initial_state)
