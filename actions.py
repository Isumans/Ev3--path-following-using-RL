"""Physical actions implemented with python-ev3dev2 motors."""

from time import sleep

from ev3dev2.button import Button
from ev3dev2.motor import SpeedPercent

from config import (
    FORWARD_SPEED_PERCENT,
    FORWARD_TIME_SECONDS,
    MAX_TURN_STEPS,
    OBSTACLE_REVERSE_SECONDS,
    OBSTACLE_REVERSE_SPEED_PERCENT,
    OBSTACLE_SCAN_DEGREES,
    OBSTACLE_SEARCH_MAX_STEPS,
    OBSTACLE_SEARCH_SPEED_PERCENT,
    OBSTACLE_SEARCH_STEP_SECONDS,
    TURN_INNER_SPEED_PERCENT,
    TURN_OUTER_SPEED_PERCENT,
    TURN_STEP_SECONDS,
)
from states import BLACK, WHITE, get_light_state

FORWARD = "FORWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
ACTIONS = (FORWARD, LEFT, RIGHT)
stop_button = Button()


def stop_requested():
    return "backspace" in stop_button.buttons_pressed


def forward(robot, light_sensor, previous_state):
    speed = SpeedPercent(FORWARD_SPEED_PERCENT)
    robot.on(speed, speed)
    remaining = FORWARD_TIME_SECONDS
    while remaining > 0:
        if stop_requested():
            raise KeyboardInterrupt
        interval = min(TURN_STEP_SECONDS, remaining)
        sleep(interval)
        remaining -= interval
    robot.off(brake=True)


def _turn_until_state_changes(
    robot, light_sensor, previous_state, left_speed, right_speed
):
    for _ in range(MAX_TURN_STEPS):
        if stop_requested():
            raise KeyboardInterrupt
        if get_light_state(light_sensor) != previous_state:
            break
        robot.on(SpeedPercent(left_speed), SpeedPercent(right_speed))
        sleep(TURN_STEP_SECONDS)
    robot.off(brake=True)


def turn_left(robot, light_sensor, previous_state):
    _turn_until_state_changes(
        robot,
        light_sensor,
        previous_state,
        TURN_INNER_SPEED_PERCENT,
        TURN_OUTER_SPEED_PERCENT,
    )


def turn_right(robot, light_sensor, previous_state):
    _turn_until_state_changes(
        robot,
        light_sensor,
        previous_state,
        TURN_OUTER_SPEED_PERCENT,
        TURN_INNER_SPEED_PERCENT,
    )


def execute_action(action, robot, light_sensor, previous_state):
    if action == FORWARD:
        forward(robot, light_sensor, previous_state)
    elif action == LEFT:
        turn_left(robot, light_sensor, previous_state)
    elif action == RIGHT:
        turn_right(robot, light_sensor, previous_state)
    else:
        raise ValueError("Unknown action: {}".format(action))


def avoid_obstacle(robot, sound, light_sensor):
    robot.on(
        SpeedPercent(OBSTACLE_REVERSE_SPEED_PERCENT),
        SpeedPercent(OBSTACLE_REVERSE_SPEED_PERCENT),
    )
    remaining = OBSTACLE_REVERSE_SECONDS
    while remaining > 0:
        if stop_requested():
            raise KeyboardInterrupt
        interval = min(OBSTACLE_SEARCH_STEP_SECONDS, remaining)
        sleep(interval)
        remaining -= interval
    robot.off(brake=True)

    if stop_requested():
        raise KeyboardInterrupt
    robot.on_for_degrees(
        SpeedPercent(-OBSTACLE_SEARCH_SPEED_PERCENT),
        SpeedPercent(OBSTACLE_SEARCH_SPEED_PERCENT),
        OBSTACLE_SCAN_DEGREES,
        brake=True,
        block=True,
    )
    left_reading = light_sensor.reflected_light_intensity

    if stop_requested():
        raise KeyboardInterrupt
    robot.on_for_degrees(
        SpeedPercent(OBSTACLE_SEARCH_SPEED_PERCENT),
        SpeedPercent(-OBSTACLE_SEARCH_SPEED_PERCENT),
        OBSTACLE_SCAN_DEGREES,
        brake=True,
        block=True,
    )

    if stop_requested():
        raise KeyboardInterrupt
    robot.on_for_degrees(
        SpeedPercent(OBSTACLE_SEARCH_SPEED_PERCENT),
        SpeedPercent(-OBSTACLE_SEARCH_SPEED_PERCENT),
        OBSTACLE_SCAN_DEGREES,
        brake=True,
        block=True,
    )
    right_reading = light_sensor.reflected_light_intensity

    if left_reading <= right_reading:
        left_speed = -OBSTACLE_SEARCH_SPEED_PERCENT
        right_speed = OBSTACLE_SEARCH_SPEED_PERCENT
    else:
        left_speed = OBSTACLE_SEARCH_SPEED_PERCENT
        right_speed = -OBSTACLE_SEARCH_SPEED_PERCENT

    saw_black = get_light_state(light_sensor) == BLACK
    for _ in range(OBSTACLE_SEARCH_MAX_STEPS):
        if stop_requested():
            raise KeyboardInterrupt
        state = get_light_state(light_sensor)
        if state == BLACK:
            saw_black = True
        elif saw_black and state == WHITE:
            break
        robot.on(SpeedPercent(left_speed), SpeedPercent(right_speed))
        sleep(OBSTACLE_SEARCH_STEP_SECONDS)

    robot.off(brake=True)
    sound.beep()

