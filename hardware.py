"""EV3 hardware initialization using python-ev3dev2."""

from ev3dev2.display import Display
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from ev3dev2.sound import Sound


robot = MoveTank(OUTPUT_A, OUTPUT_B)
light_sensor = ColorSensor(INPUT_1)
light_sensor.mode = ColorSensor.MODE_COL_REFLECT
ir_sensor = InfraredSensor(INPUT_4)
ir_sensor.mode = InfraredSensor.MODE_IR_PROX
display = Display()
sound = Sound()

