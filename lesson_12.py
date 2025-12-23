# Monadic state
import pure_robot


class State:
    def __init__(self, run):
        self.run = run

    def __call__(self, state):
        return self.run(state)

    def bind(self, f):
        def run(state):
            a, new_state = self.run(state)
            return f(a).run(new_state)

        return State(run)

    def then(self, next_state):
        return self.bind(lambda _: next_state)


def monadic_move(dist):
    def run(state):
        new_state = pure_robot.move(pure_robot.transfer_to_cleaner, dist, state)
        return None, new_state

    return State(run)


def monadic_turn(angle):
    def run(state):
        new_state = pure_robot.turn(pure_robot.transfer_to_cleaner, angle, state)
        return None, new_state

    return State(run)


def monadic_set(mode):
    def run(state):
        new_state = pure_robot.set_state(pure_robot.transfer_to_cleaner, mode, state)
        return None, new_state

    return State(run)


def monadic_start():
    def run(state):
        new_state = pure_robot.start(pure_robot.transfer_to_cleaner, state)
        return None, new_state

    return State(run)


def monadic_stop():
    def run(state):
        new_state = pure_robot.stop(pure_robot.transfer_to_cleaner, state)
        return None, new_state

    return State(run)


program = (
    monadic_move(100)
    .then(monadic_turn(-90))
    .then(monadic_set('soap'))
    .then(monadic_start())
    .then(monadic_move(50))
    .then(monadic_stop())
)

initial_state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
program.run(initial_state)
