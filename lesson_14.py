# Event sourcing
import pure_robot


class EventStore:
    def __init__(self):
        self._events = {}

    def append(self, robot_id, events):
        self._events.setdefault(robot_id, []).extend(events)

    def load(self, robot_id):
        return list(self._events.get(robot_id, []))


class Event:
    pass


class Moved(Event):
    def __init__(self, dist):
        self.dist = dist


class Turned(Event):
    def __init__(self, angle):
        self.angle = angle


class ModeSet(Event):
    def __init__(self, mode):
        self.mode = mode


class Started(Event):
    pass


class Stopped(Event):
    pass


def apply_event(event, state):
    if isinstance(event, Moved):
        return pure_robot.move(lambda _: None, event.dist, state)

    if isinstance(event, Turned):
        return pure_robot.turn(lambda _: None, event.angle, state)

    if isinstance(event, ModeSet):
        return pure_robot.set_state(lambda _: None, event.mode, state)

    if isinstance(event, Started):
        return pure_robot.start(lambda _: None, state)

    if isinstance(event, Stopped):
        return pure_robot.stop(lambda _: None, state)

    return state


def rebuild_state(events):
    state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)
    for e in events:
        state = apply_event(e, state)
    return state


class CommandHandler:
    def __init__(self, event_store):
        self.event_store = event_store

    def handle(self, robot_id, command):
        past_events = self.event_store.load(robot_id)
        state = rebuild_state(past_events)

        new_events = []

        cmd = command.split()

        if cmd[0] == "move":
            new_events.append(Moved(int(cmd[1])))

        elif cmd[0] == "turn":
            new_events.append(Turned(int(cmd[1])))

        elif cmd[0] == "set":
            new_events.append(ModeSet(cmd[1]))

        elif cmd[0] == "start":
            new_events.append(Started())

        elif cmd[0] == "stop":
            new_events.append(Stopped())

        self.event_store.append(robot_id, new_events)


def execute(robot_id, event_store):
    events = event_store.load(robot_id)
    state = pure_robot.RobotState(0.0, 0.0, 0, pure_robot.WATER)

    for e in events:
        if isinstance(e, Moved):
            state = pure_robot.move(pure_robot.transfer_to_cleaner, e.dist, state)
        elif isinstance(e, Turned):
            state = pure_robot.turn(pure_robot.transfer_to_cleaner, e.angle, state)
        elif isinstance(e, ModeSet):
            state = pure_robot.set_state(pure_robot.transfer_to_cleaner, e.mode, state)
        elif isinstance(e, Started):
            state = pure_robot.start(pure_robot.transfer_to_cleaner, state)
        elif isinstance(e, Stopped):
            state = pure_robot.stop(pure_robot.transfer_to_cleaner, state)

    return state



store = EventStore()
handler = CommandHandler(store)

robot_id = "robot-1"

handler.handle(robot_id, "move 100")
handler.handle(robot_id, "turn -90")
handler.handle(robot_id, "set soap")
handler.handle(robot_id, "start")
handler.handle(robot_id, "move 50")
handler.handle(robot_id, "stop")

final_state = execute(robot_id, store)
print(final_state)