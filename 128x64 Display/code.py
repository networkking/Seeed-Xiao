import board
import time
from busio import I2C
from digitalio import DigitalInOut
import adafruit_character_lcd.Character_LCD_I2C as cl
import adafruit_ssd1306

        #setup the boards SDA and SCL pins to use I2C
            # same as doing D5, and D4
i2c = I2C(board.SCL, board.SDA)
#i2c = board.I2C()

                            # Create a reset on pin digital pin 5
reset_pin = DigitalInOut(board.D0)

                            # screen size
                            # 0x60, # , reset=reset_pin
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=reset_pin)

print("pixel test")

display.fill(0)
display.show()

def dots():
    print("dots")
                #row 0, column 0, value 1
    display.pixel(0,0,1)
    display.pixel(display.width // 2, display.height // 2, 1)
    display.pixel(display.width - 1, display.height -1, 1) 
    display.show()
    time.sleep(1)
    
def lines():
    print("lines")
    corners = (
        (0, 0),
        (0, display.height - 1),
        (display.width - 1, 0),
        (display.width - 1, display.height - 1)
    )
    display.fill(0)
    for corner_from in corners:
        for corner_to in corners:
            display.line(corner_from[0], corner_from[1], corner_to[0], corner_to[1], 1) # This will need to get finished
    display.show()
    time.sleep(1)
def inverse_lines():
    print("Inverse Lines")
    corners = (
        (0, 0),
        (0, display.height - 1),
        (display.width - 1, 0),
        (display.width - 1, display.height - 1)
    )
    display.fill(1)
    for corner_from in corners:
        for corner_to in corners:
            display.line(corner_from[0], corner_from[1], corner_to[0], corner_to[1], 0) # This will need to get finished
    display.show()
    time.sleep(1)
def rectangles():
    print("rectanle test")
    display.fill(0)
    w_delta = display.width / 10
    h_delta = display.height / 10
    for i in range(11):
        display.rect(0,0,int(w_delta * i), int(h_delta * i), 1)
    display.show()
    time.sleep(1)

def text():
    print("Text test")
    display.fill(0)
    try:
        display.text("I LOVE", 0, 0, 1)
        display.text("MY", 0, 9, 1)
        display.text("WIFE", 0, 20, 1)
        display.text("REBEKAH", 0, 30, 1)
        display.text("ARLENE", 0, 38, 1)
        display.text("LUNDBERG", 0, 46  , 1)

        display.show()
        time.sleep(3)
        display.fill(1)
        char_width = 6
        char_height = 8
        chars_per_line = display.width//6
        for i in range(255):
            x = char_width * (i % chars_per_line)
            y = char_height * (i // chars_per_line)
            display.text(chr(i), x, y, 1)
        display.show()
    except FileNotFoundError:
        print("To test the framebuf font setup, you'll need the font5x8.bin file https://github.com/adafruit/Adafruit_CircuitPython_framebuf/Tree in the same directory as this script")
    time.sleep(1)

def inverse_text():
    print("Inverse Text")
    display.fill(1)
    try:
        display.text("I LOVE", 0, 0, 0)
        display.text("MY", 0, 9, 0)
        display.text("WIFE", 0, 20, 0)
        display.text("REBEKAH", 0, 30, 0)
        display.text("ARLENE", 0, 38, 0)
        display.text("LUNDBERG", 0, 46, 0)

        display.show()
        time.sleep(3)
        display.fill(1)
        char_width = 6
        char_height = 8
        chars_per_line = display.width//6
        for i in range(255):
            x = char_width * (i % chars_per_line)
            y = char_height * (i // chars_per_line)
            display.text(chr(i), x, y, 1)
        display.show()
    except FileNotFoundError:
        print("To test the framebuf font setup, you'll need the font5x8.bin file https://github.com/adafruit/Adafruit_CircuitPython_framebuf/Tree in the same directory as this script")
    time.sleep(1)



increment = 0


while increment < 10:
    dots()
    lines()
    inverse_lines()
    rectangles()
    text()
    inverse_text()
    display.fill(0)
    display.show()
    increment += 1
    print(increment)