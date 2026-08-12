"""Physical actions implemented with python-ev3dev2 motors."""

from time import sleep

from ev3dev2.motor import SpeedPercent

from config import (
    FORWARD_SPEED_PERCENT,
    FORWARD_TIME_SECONDS,
    MAX_TURN_STEPS,
    OBSTACLE_TURN_DEGREES,
    OBSTACLE_TURN_STEPS,
    TURN_INNER_SPEED_PERCENT,
    TURN_OUTER_SPEED_PERCENT,
    TURN_STEP_SECONDS,
)
from states import get_light_state

FORWARD = "FORWARD"
LEFT = "LEFT"
RIGHT = "RIGHT"
ACTIONS = (FORWARD, LEFT, RIGHT)


def forward(robot, light_sensor, previous_state):
    speed = SpeedPercent(FORWARD_SPEED_PERCENT)
    robot.on(speed, speed)
    sleep(FORWARD_TIME_SECONDS)
    robot.off(brake=True)


def _turn_until_state_changes(
    robot, light_sensor, previous_state, left_speed, right_speed
):
    for _ in range(MAX_TURN_STEPS):
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


def avoid_obstacle(robot, sound, mode):
    direction = -1 if mode else 1
    for _ in range(OBSTACLE_TURN_STEPS):
        robot.on_for_degrees(
            SpeedPercent(direction * 20),
            SpeedPercent(direction * -20),
            OBSTACLE_TURN_DEGREES,
            brake=True,
            block=True,
        )
        sound.beep()

