import board
import time
from busio import I2C
from digitalio import DigitalInOut, Direction, Pull

btn1 = DigitalInOut(board.D0)
btn1.direction = Direction.INPUT
btn1.pull = Pull.DOWN
btn2 = DigitalInOut(board.D1)
btn2.direction = Direction.INPUT
btn2.pull = Pull.DOWN
increment = 0
while increment < 100:
    print(f"button 1 value: {btn1.value}")
    print(f"button 2 value: {btn2.value}")
    time.sleep(.5)

    increment += 1
    print(f"increment = {increment}")