# concatenative_robot.py
import math
from collections import namedtuple

RobotState = namedtuple("RobotState", "x y angle state")

WATER = 1
SOAP = 2
BRUSH = 3

def transfer_to_cleaner(message):
    print(message)

def cmd_move(stack, state):
    dist = stack.pop()
    angle_rads = state.angle * (math.pi/180.0)
    new_state = RobotState(
        state.x + dist * math.cos(angle_rads),
        state.y + dist * math.sin(angle_rads),
        state.angle,
        state.state
    )
    transfer_to_cleaner(("POS(", new_state.x, ",", new_state.y, ")"))
    return new_state

def cmd_turn(stack, state):
    turn_angle = stack.pop()
    new_state = RobotState(
        state.x,
        state.y,
        state.angle + turn_angle,
        state.state
    )
    transfer_to_cleaner(("ANGLE", new_state.angle))
    return new_state

def cmd_set(stack, state):
    mode = stack.pop()
    if mode == "water":
        m = WATER
    elif mode == "soap":
        m = SOAP
    elif mode == "brush":
        m = BRUSH
    else:
        return state
    new_state = RobotState(state.x, state.y, state.angle, m)
    transfer_to_cleaner(("STATE", m))
    return new_state

def cmd_start(state):
    transfer_to_cleaner(("START WITH", state.state))
    return state

def cmd_stop(state):
    transfer_to_cleaner(("STOP",))
    return state

OPS = {
    "move": cmd_move,
    "turn": cmd_turn,
    "set": cmd_set,
    "start": cmd_start,
    "stop": cmd_stop,
}

def interpret(stream, state):
    stack = []
    for token in stream.split():
        if token in OPS:
            state = OPS[token](stack, state)
        else:
            try:
                stack.append(int(token))
            except:
                stack.append(token)
    return state



interpret("100 move -90 turn soap set start 50 move stop", RobotState(0, 0, 0, WATER))
