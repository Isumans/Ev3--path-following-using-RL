"""Q-table creation, selection, and Q-learning update."""

import math
import random

from actions import ACTIONS
from config import ALPHA, GAMMA, TEMPERATURE
from states import LIGHT_STATES

MODES = (True, False)


def create_q_table():
    return {
        (mode, light_state, action): 0.0
        for mode in MODES
        for light_state in LIGHT_STATES
        for action in ACTIONS
    }


def get_best_action(q_table, mode, light_state):
    best_action = ACTIONS[0]
    best_value = q_table[(mode, light_state, best_action)]
    for action in ACTIONS[1:]:
        value = q_table[(mode, light_state, action)]
        if value > best_value:
            best_action = action
            best_value = value
    return best_action, best_value


def exploration_rate(iteration):
    return math.exp(-iteration / TEMPERATURE)


def choose_action(q_table, mode, light_state, epsilon):
    if random.random() < epsilon:
        return random.choice(ACTIONS), True
    return get_best_action(q_table, mode, light_state)[0], False


def update_q_value(q_table, mode, state, action, reward, new_mode, new_state):
    key = (mode, state, action)
    old_value = q_table[key]
    best_future_value = get_best_action(q_table, new_mode, new_state)[1]
    target = reward + GAMMA * best_future_value
    q_table[key] = old_value + ALPHA * (target - old_value)

