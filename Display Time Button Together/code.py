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
    # (tm_year=2022, tm_mon=9, tm_mday=15, tm_hour=17, tm_min=15, tm_sec=22, tm_wday=3, tm_yday=-1, tm_isdst=-1
    year_len = len(f"{ct.tm_year}")
    display.text(f"{ct.tm_year}", (display.width//2-year_len*2)-6, 0, 1)
    day_len = len(f"{days[ct.tm_wday]}")
    display.text(f"{days[ct.tm_wday]}", (display.width//2-day_len*2)-6, 16, 1)
    time_len = len(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}")
    display.text(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}", (display.width//2-time_len*2)-6, 24, 1)
    display.show()




def button_1_function(menu):
    display.fill(0)
    x = 0
    y = 16
    display.text("MENU", (display.width//2-len("MENU")*2)-8, 0, 1)
    for option in menu:
        display.text(f"{option}", x, y, 1)
        y += 8
    display.show()
    time.sleep(5)
    state.pop()


def button_2_function(words):
    display.fill(0)
    display.text(f"{words}", 0, 16, 1)
    display.circle()
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
menu = ["Set Time", "Change Color", "Timer", "Alarm"]
display.fill(0)

while True:

    get_input()  # no change if no button pushed
    if state[-1] == display_time:
        current_time = rtc.datetime
        state[-1](current_time)

    elif state[-1] != display_time:
        if state[-1] == button_1_function:
            state[-1](menu)
        if state[-1] == button_2_function:
            state[-1]("Button 2 was pressed")







    display.show()
    if time_pushed + 5 == time.time()
        state.pop()