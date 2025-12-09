import pure_robot


class RobotApi:
    def setup(self, f_command, f_transfer):
        self.f_command = f_command
        self.f_transfer = f_transfer

    def make(self, command):
        if not hasattr(self, 'cleaner_state'):
            self.cleaner_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

        cmd = command.split(' ')
        cmd_type = cmd[0]

        if cmd_type == 'move':
            self.cleaner_state = self.f_command(
                self.f_transfer, cmd_type, self.cleaner_state, int(cmd[1])
            )
        elif cmd_type == 'turn':
            self.cleaner_state = self.f_command(
                self.f_transfer, cmd_type, self.cleaner_state, int(cmd[1])
            )
        elif cmd_type == 'set':
            self.cleaner_state = self.f_command(
                self.f_transfer, cmd_type, self.cleaner_state, cmd[1]
            )
        elif cmd_type in ('start', 'stop'):
            self.cleaner_state = self.f_command(
                self.f_transfer, cmd_type, self.cleaner_state
            )

        return self.cleaner_state

    def __call__(self, command):
        return self.make(command)


def transfer_to_cleaner(message):
    print(message)


def universal_command(transfer, cmd_type, state, *args):
    if cmd_type == 'move':
        return pure_robot.move(transfer, args[0], state)
    elif cmd_type == 'turn':
        return pure_robot.turn(transfer, args[0], state)
    elif cmd_type == 'set':
        return pure_robot.set_state(transfer, args[0], state)
    elif cmd_type == 'start':
        return pure_robot.start(transfer, state)
    elif cmd_type == 'stop':
        return pure_robot.stop(transfer, state)
    else:
        raise ValueError(f"Unknown command type: {cmd_type}")


def double_move_command(transfer, cmd_type, state, *args):
    if cmd_type == 'move':
        return pure_robot.move(transfer, args[0] * 2, state)
    else:
        return universal_command(transfer, cmd_type, state, *args)


api = RobotApi()
api.setup(universal_command, transfer_to_cleaner)

api('move 100')
api('turn -90')
api('set soap')
api('start')
api('move 50')
s = api('stop')