"""Convert reflection readings and transitions into RL states."""

from config import BLACK_VALUE, WHITE_VALUE

WHITE = "WHITE"
MIDDLE = "MIDDLE"
BLACK = "BLACK"
LIGHT_STATES = (WHITE, MIDDLE, BLACK)

MODE_TRUE_TRANSITIONS = (
    (MIDDLE, "RIGHT", WHITE),
    (WHITE, "LEFT", MIDDLE),
    (MIDDLE, "LEFT", BLACK),
    (BLACK, "RIGHT", MIDDLE),
)

MODE_FALSE_TRANSITIONS = (
    (MIDDLE, "RIGHT", BLACK),
    (BLACK, "LEFT", MIDDLE),
    (MIDDLE, "LEFT", WHITE),
    (WHITE, "RIGHT", MIDDLE),
)


def get_light_state(light_sensor):
    reading = light_sensor.reflected_light_intensity
    if reading >= WHITE_VALUE:
        return WHITE
    if reading <= BLACK_VALUE:
        return BLACK
    return MIDDLE


def update_mode(mode, old_state, action, new_state):
    transition = (old_state, action, new_state)
    if transition in MODE_TRUE_TRANSITIONS:
        return True
    if transition in MODE_FALSE_TRANSITIONS:
        return False
    return mode

