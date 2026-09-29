#!/usr/bin/env python3
"""Follow the line using a Q-table trained with python-ev3dev2."""

from actions import RIGHT, avoid_obstacle, execute_action, stop_requested
from config import OBSTACLE_PROXIMITY
from hardware import ir_sensor, light_sensor, robot, sound
from qlearning import get_best_action
from states import get_light_state, update_mode
from storage import load_q_table


def find_initial_mode(mode, light_state):
    action = RIGHT
    execute_action(action, robot, light_sensor, light_state)
    new_state = get_light_state(light_sensor)
    return update_mode(mode, light_state, action, new_state), new_state


def run():
    q_table = load_q_table()
    mode = True
    light_state = get_light_state(light_sensor)
    mode, light_state = find_initial_mode(mode, light_state)

    try:
        while True:
            if stop_requested():
                raise KeyboardInterrupt
            if ir_sensor.proximity < OBSTACLE_PROXIMITY:
                sound.speak("Avoiding obstacle")
                avoid_obstacle(robot, sound, light_sensor)
                light_state = get_light_state(light_sensor)
                continue

            action = get_best_action(q_table, mode, light_state)[0]
            print("line following", mode, action, light_state)
            execute_action(action, robot, light_sensor, light_state)
            new_state = get_light_state(light_sensor)
            mode = update_mode(mode, light_state, action, new_state)
            light_state = new_state
    except KeyboardInterrupt:
        print("Line following stopped")
    finally:
        robot.off(brake=True)


if __name__ == "__main__":
    run()

