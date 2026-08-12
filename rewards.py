"""Reward function for line following."""

from states import MIDDLE


def get_reward(light_state):
    return 10 if light_state == MIDDLE else -10

