#!/usr/bin/env python3
"""Train a Q-table using standard Python and python-ev3dev2."""

from actions import execute_action
from config import MIN_EPSILON
from hardware import display, light_sensor, robot, sound
from qlearning import (
    choose_action,
    create_q_table,
    exploration_rate,
    update_q_value,
)
from rewards import get_reward
from states import get_light_state, update_mode
from storage import load_checkpoint, save_checkpoint, save_q_table


def show_progress(iteration, epsilon):
    display.clear()
    display.text_grid("Training", x=7, y=2, clear_screen=False)
    display.text_grid("Step: {}".format(iteration), x=3, y=5, clear_screen=False)
    display.text_grid("E: {:.3f}".format(epsilon), x=3, y=7, clear_screen=False)
    display.update()


def restore_training_state():
    checkpoint = load_checkpoint()
    if checkpoint is None:
        print("No checkpoint found; starting new training")
        return create_q_table(), 0, True
    print("Resuming training from step", checkpoint["iteration"])
    return checkpoint["q_table"], checkpoint["iteration"], checkpoint["mode"]


def train():
    q_table, iteration, mode = restore_training_state()
    light_state = get_light_state(light_sensor)

    try:
        while True:
            epsilon = exploration_rate(iteration)
            if epsilon < MIN_EPSILON:
                break

            action, exploring = choose_action(q_table, mode, light_state, epsilon)
            print("random" if exploring else "greedy", action, mode, light_state)

            execute_action(action, robot, light_sensor, light_state)
            new_light_state = get_light_state(light_sensor)
            new_mode = update_mode(mode, light_state, action, new_light_state)
            reward = get_reward(new_light_state)
            update_q_value(
                q_table,
                mode,
                light_state,
                action,
                reward,
                new_mode,
                new_light_state,
            )

            light_state = new_light_state
            mode = new_mode
            iteration += 1
            show_progress(iteration, epsilon)
            save_checkpoint(q_table, iteration, mode)
    except KeyboardInterrupt:
        print("Training stopped at step", iteration)
    finally:
        robot.off(brake=True)
        save_checkpoint(q_table, iteration, mode)

    if exploration_rate(iteration) < MIN_EPSILON:
        save_q_table(q_table)
        sound.speak("Training complete").wait()


if __name__ == "__main__":
    train()

