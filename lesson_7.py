#Stateless
import pure_robot


class CleanerApi:
    def __init__(self):
        pass

    def activate_cleaner(self, code, state):
        robot_state = state
        for command in code:
            cmd = command.split(' ')
            if cmd[0] == 'move':
                robot_state = pure_robot.move(pure_robot.transfer_to_cleaner, int(cmd[1]), robot_state)
            elif cmd[0] == 'turn':
                robot_state = pure_robot.turn(pure_robot.transfer_to_cleaner, int(cmd[1]), robot_state)
            elif cmd[0] == 'set':
                robot_state = pure_robot.set_state(pure_robot.transfer_to_cleaner, cmd[1], robot_state)
            elif cmd[0] == 'start':
                robot_state = pure_robot.start(pure_robot.transfer_to_cleaner, robot_state)
            elif cmd[0] == 'stop':
                robot_state = pure_robot.stop(pure_robot.transfer_to_cleaner, robot_state)

        return robot_state


# Храним состояние на клиенте
state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
bot = CleanerApi()

bot.activate_cleaner((
    'move 100',
    'turn -90',
    'set soap',
    'start',
    'move 50',
    'stop'
), state)
