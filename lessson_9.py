# Functional injection
# Реализована функциональная инъекция через конструктор класса
# Плюсы
# Теперь мы не зависим от реализации конкретного интерфейса и можем
# вносить изменения в отдельные функции
# Минусы
# Приходится последовательно передовать все функции в конструктор
import pure_robot


def transfer_to_cleaner(message):
    print(message)


class RobotApi:
    def __init__(self, transfer, move, turn, set_state, start, stop):
        self.transfer_to_cleaner = transfer
        self.move = move
        self.turn = turn
        self.set_state = set_state
        self.start = start
        self.stop = stop

    def run(self, command, state):
        cmd = command.split(' ')
        if cmd[0] == 'move':
            state = self.move(self.transfer_to_cleaner, int(cmd[1]), state)
        elif cmd[0] == 'turn':
            state = self.turn(self.transfer_to_cleaner, int(cmd[1]), state)
        elif cmd[0] == 'set':
            state = self.set_state(self.transfer_to_cleaner, cmd[1], state)
        elif cmd[0] == 'start':
            state = self.start(self.transfer_to_cleaner, state)
        elif cmd[0] == 'stop':
            state = self.stop(self.transfer_to_cleaner, state)
        return state


robot = RobotApi(transfer_to_cleaner, pure_robot.move,
                 pure_robot.turn,
                 pure_robot.set_state,
                 pure_robot.start,
                 pure_robot.stop)

state = pure_robot.RobotState(0, 0, 0, pure_robot.WATER)

state = robot.run("move 100", state)
state = robot.run("turn -90", state)
state = robot.run("set soap", state)
state = robot.run("start", state)
state = robot.run("move 50", state)
state = robot.run("stop", state)
