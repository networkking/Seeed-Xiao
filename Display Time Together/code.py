import board
import time
from busio import I2C
from digitalio import DigitalInOut
import adafruit_character_lcd.Character_LCD_I2C as cl
import adafruit_ssd1306
import adafruit_ds1307

i2c = I2C(board.SCL, board.SDA)
rtc = adafruit_ds1307.DS1307(i2c)

reset_pin = DigitalInOut(board.D0)

display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=reset_pin)
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday", }


def text(ct):
    display.fill(0)

    # (tm_year=2022, tm_mon=9, tm_mday=15, tm_hour=17, tm_min=15, tm_sec=22, tm_wday=3, tm_yday=-1, tm_isdst=-1)

    try:  # x  #y #on/off
        year_len = len(f"{ct.tm_year}")
        display.text(f"{ct.tm_year}", 46, 0, 1)
        day_len = len(f"{days[ct.tm_wday]}")
        display.text(f"{days[ct.tm_wday]}", 32 + day_len, 16, 1)
        time_len = len(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}")
        # yellow starts at 15
        display.text(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}", 32 + time_len, 24, 1)

        display.show()
        display.fill(1)
        char_width = 6
        char_height = 8
        chars_per_line = display.width // 6
        for i in range(255):
            x = char_width * (i % chars_per_line)
            y = char_height * (i // chars_per_line)
            display.text(chr(i), x, y, 1)
        display.show()
    except FileNotFoundError:
        print(
            "To test the framebuf font setup, you'll need the font5x8.bin file https://github.com/adafruit/Adafruit_CircuitPython_framebuf/Tree in the same directory as this script")
        time.sleep(1)


while True:
    current_time = rtc.datetime
    text(current_time)
