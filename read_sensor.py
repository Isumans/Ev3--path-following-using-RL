#!/usr/bin/env python3
"""Show reflected-light values on the EV3 screen and terminal."""

from time import sleep

from hardware import display, light_sensor


try:
    while True:
        reflection = light_sensor.reflected_light_intensity
        print("Reflection:", reflection)
        display.clear()
        display.text_grid("Reflection", x=6, y=3, clear_screen=False)
        display.text_grid(str(reflection), x=10, y=6, clear_screen=False)
        display.update()
        sleep(0.5)
except KeyboardInterrupt:
    pass

