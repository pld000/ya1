import pure_robot
def transfer_to_cleaner(message):
    print(message)

def robot_api(transfer):
    def do_move(dist, state):
        return pure_robot.move(transfer, dist, state)

    def do_turn(angle, state):
        return pure_robot.turn(transfer, angle, state)

    def do_set(mode, state):
        return pure_robot.set_state(transfer, mode, state)

    def do_start(state):
        return pure_robot.start(transfer, state)

    def do_stop(state):
        return pure_robot.stop(transfer, state)

    def run(program, state):
        return pure_robot.make(transfer, program, state)

    return {
        "move": do_move,
        "turn": do_turn,
        "set": do_set,
        "start": do_start,
        "stop": do_stop,
        "run": run,
    }

api = robot_api(transfer_to_cleaner)

state = pure_robot.RobotState(0, 0, 0, pure_robot.WATER)

state = api["run"]([
    "move 100",
    "turn -90",
    "set soap",
    "start",
    "move 50",
    "stop",
], state)