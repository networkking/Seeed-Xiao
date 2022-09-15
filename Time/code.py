# waiting on time board for this
import board
import time
import adafruit_ds1307

from busio import I2C
from digitalio import DigitalInOut

i2c = I2C(board.SCL, board.SDA)

rtc = adafruit_ds1307.DS1307(i2c)
# This sets the datetime. So you'd have to do this if it ever lost power.
#rtc.datetime = time.struct_time((2022, 9, 15, 17, 9, 0, 3, 258, 1))


# This prints the current time
r = rtc.datetime
print(r)