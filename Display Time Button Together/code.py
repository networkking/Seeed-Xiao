import board
import time
from busio import I2C
from digitalio import DigitalInOut, Direction, Pull
import adafruit_character_lcd.Character_LCD_I2C as cl
import adafruit_ssd1306
import adafruit_ds1307

# Setting up board
i2c = I2C(board.SCL, board.SDA)
rtc = adafruit_ds1307.DS1307(i2c)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)
button1 = DigitalInOut(board.D0)
button1.direction = Direction.INPUT
button1.pull = Pull.DOWN
button2 = DigitalInOut(board.D1)
button2.direction = Direction.INPUT
button2.pull = Pull.DOWN


def display_time(ct):
    display.fill(0)

    # (tm_year=2022, tm_mon=9, tm_mday=15, tm_hour=17, tm_min=15, tm_sec=22, tm_wday=3, tm_yday=-1, tm_isdst=-1)

    try:  # x  #y #on/off

        display.text(f"{ct.tm_year}", 46, 0, 1)
        day_len = len(f"{days[ct.tm_wday]}")
        display.text(f"{days[ct.tm_wday]}", 32 + day_len, 16, 1)
        time_len = len(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}")
        # yellow starts at 15
        display.text(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}", 32 + time_len, 24, 1)
        display.show()

        # Not sure what this does
        char_width = 6
        char_height = 8
        chars_per_line = display.width // 6
        for i in range(255):
            x = char_width * (i % chars_per_line)
            y = char_height * (i // chars_per_line)
            display.text(chr(i), x, y, 1)
    except FileNotFoundError:
        print(
            "To test the framebuf font setup, you'll need the font5x8.bin file https://github.com/adafruit/Adafruit_CircuitPython_framebuf/Tree in the same directory as this script")
        time.sleep(1)


def button_1_function(words):
    display.fill(0)
    display.display_time(f"{words}", 46, 0, 1)
    display.show()
    time.sleep(5)
    state.pop()


def button_2_function(words):
    display.fill(0)
    display.text(f"{words}", 46, 0, 1)
    display.show()
    time.sleep(5)
    state.pop()


def get_input():
    if button1.value:
        print("Button pressed")
        state.append(button_1_function)
    elif button2.value:
        print("Button pressed")
        state.append(button_2_function)


# Setting in variables
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
state = [display_time]
display.fill(0)

while True:

    get_input()  # no change if no button pushed
    if state[-1] == display_time:
        current_time = rtc.datetime
        state[-1](current_time)

    elif state[-1] != display_time:
        if "1" in state[-1]:
            state[-1]("Button 1 was pressed")
        elif "2" in state[-1]:
            state[-1]("Button 2 was pressed")