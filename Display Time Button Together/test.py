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
button3 = DigitalInOut(board.D2)
button3.direction = Direction.INPUT
button3.pull = Pull.DOWN
button4 = DigitalInOut(board.D3)
button4.direction = Direction.INPUT
button4.pull = Pull.DOWN


def display_time(ct, alarm_hour, alarm_min, alarm_set):
    display.fill(0)
    # (tm_year=2022, tm_mon=9, tm_mday=15, tm_hour=17, tm_min=15, tm_sec=22, tm_wday=3, tm_yday=-1, tm_isdst=-1
    if alarm_set:
        if ct.tm_hour == alarm_hour and ct.tm_min == alarm_min:
            state.pop()
            state.appened(flash_alarm)
    year_len = len(f"{ct.tm_year}")
    display.text(f"{ct.tm_year}", (display.width // 2 - year_len * 4) - 8, 0, 1, size=2)
    day_len = len(f"{days[ct.tm_wday]}")
    display.text(f"{days[ct.tm_wday]}", (display.width // 2 - day_len * 2) - 6, 16, 1)
    time_len = len(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}")
    display.text(f"{ct.tm_hour}:{ct.tm_min}:{ct.tm_sec}", (display.width // 2 - time_len * 4) - 12, 28, 1, size=2)
    display.show()


def menu_func(menu):
    global circle_y_location
    global timer_clock
    display.fill(0)
    x = 10
    y = 16
    display.text("MENU", (display.width // 2 - len("MENU") * 2) - 8, 0, 1)
    for option in menu:
        display.text(f"{option}", x, y, 1)
        y += 8
    display.circle(4, circle_y_location, 4, 1)
    display.show()
    if button1.value:
        state.pop()
        time.sleep(1)
        return

    if button2.value:
        if circle_y_location == 43:
            circle_y_location = 11
        circle_y_location += 8

    if button3.value:
        state.pop()
        print(circle_y_location)
        if circle_y_location == 19:
            state.append(set_time)
        if circle_y_location == 27:
            state.append(change_color)
        if circle_y_location == 35:
            timer_clock = time.time()
            state.append(timer)
        if circle_y_location == 43:
            state.append(alarm)


def set_time():
    print("This will no be implimented")


def change_color():
    print("This will not be implimented till I get a different screen")


def timer(start_time):
    global new_timer
    ticker = (time.time() - start_time)
    display.fill(0)
    display.text("Timer", 65, 0, 1)
    x_location = 79 - (len(str(ticker)) * 2)
    display.text(f"{ticker}", x_location, 37, 1)
    display.circle(80, 40, 24, 1)
    laps_x = 0
    laps_y = 16
    scrolling = 0
    if len(laps) > 0:
        if len(laps) > 6:
            scrolling = len(laps) - 6
            laps_y -= 8 * scrolling
        for index, lap in enumerate(laps):
            display.text(f"#{str(index + 1)}: {str(lap)}", laps_x, laps_y, 1)
            laps_y += 8
    display.show()
    if button1.value:
        state.pop()
        time.sleep(1)
        return
    if button4.value:
        if len(laps) == 0:
            new_timer += ticker
            laps.append(ticker)
        elif len(laps) >= 1:
            new_timer += laps[-1]
            laps.append(ticker - new_timer)


def alarm(hour, min, set, ct):
    display.fill(0)
    text = "Set Alarm"
    display.text(text, 32, 0, 1)
    display.text(f"Current Time {ct.tm_hour}:{ct.tm_min}", 10, 20, 1)
    display.text(f"hour: {hour}", 10, 32, 1, size=2)
    display.text(f" min: {min}", 10, 48, 1, size=2)
    display.show()
    if button1.value:
        state.pop()
        time.sleep(1)
        set = True
        return hour, min, set
    if button2.value:
        display.text(f"EXIT", 10, 32, 1, size=2)
        time.sleep(1)
        set = False
        state.pop()
        return hour, min, set
    if button3.value:
        hour += 1
        if hour > 23: hour = 0
    if button4.value:
        if min > 59: min = 0
        min += 1
    return hour, min, alarm_set


def flash_alarm():
    display.fill(1)
    display.show()
    display.fill(0)
    display.show()
    if button1.value:
        state.pop()
        return


def button_2_function(words):
    display.fill(0)
    display.text(f"{words}", 0, 16, 1)
    display.circle(64, 32, 6, 1)
    display.show()
    if button1.value:
        state.pop()
        time.sleep(1)
        return


def get_input():
    if button1.value:
        state.append(menu_func)
    elif button2.value:
        state.append(button_2_function)


# Setting in variables
days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday", }
state = [display_time]
menu = ["Set Time", "Change Color", "Timer", "Alarm"]
display.fill(0)
circle_y_location = 19
timer_clock = 0
laps = []
new_timer = 0
alarm_hour = 0
alarm_min = 0
alarm_set = False
while True:

    if state[-1] == display_time:
        get_input()
        current_time = rtc.datetime
        state[-1](current_time, alarm_hour, alarm_min, alarm_set)

    elif state[-1] != display_time:
        if state[-1] == menu_func:
            state[-1](menu)
        elif state[-1] == button_2_function:
            state[-1]("Button 2 was pressed")
        elif state[-1] == set_time:
            pass
        elif state[-1] == change_color:
            pass
        elif state[-1] == timer:
            state[-1](timer_clock)
        elif state[-1] == alarm:
            alarm_hour, alarm_min, alarm_set = state[-1](alarm_hour, alarm_min, alarm_set, rtc.datetime)
        elif state[-1] == flash_alarm:
            state[-1]()
    display.show()
