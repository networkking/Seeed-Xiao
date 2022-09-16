import board
import time
import adafruit_ds1307

from busio import I2C
from digitalio import DigitalInOut

i2c = I2C(board.SCL, board.SDA)

rtc = adafruit_ds1307.DS1307(i2c)


# Set time on RTC
rtc.datetime = time.struct_time((2022, 9, 16, 11, 17, 0, 4, 259, 1))

r = rtc.datetime
print(r)