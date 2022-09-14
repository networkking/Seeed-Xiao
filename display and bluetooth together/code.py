import board
import time
from busio import I2C
from digitalio import DigitalInOut
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.location_packet import LocationPacket
import adafruit_ssd1306


i2c = I2C(board.SCL, board.SDA)
reset_pin = DigitalInOut(board.D0)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=reset_pin)
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.name = "Smart Watch"

display.fill(0)
display.show()

print("i2c module", dir(i2c))
print("ble module", dir(ble))
print("uart module", dir(uart))
print("advertisement module", dir(advertisement))
def text(lat, lon, alt):

    try:
        display.fill(0)
        display.text(f"Latitude is {lat}", 0, 0, 1)
        display.text(f"Longitude is {lon}", 0, 9, 1)
        display.text(f"Altitude is {alt}", 0, 20, 1)
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
        print("To test the framebuf font setup, you'll need the font5x8.bin file https://github.com/adafruit/Adafruit_CircuitPython_framebuf/Tree in the same directory as this script")


def connect_with_bluetooth():
    # Try to connect
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass  # Do this while not connected to a device
    while ble.connected:
        if uart.in_waiting:
            try:
                packet = Packet.from_stream(uart)
                if isinstance(packet, LocationPacket):
                    text(packet.latitude, packet.longitude, packet.altitude)
            except ValueError:
                print("""Issue with checksum in   File "adafruit_bluefruit_connect/packet.py", line 121, in from_stream
    File "adafruit_bluefruit_connect/packet.py", line 73, in from_bytes""")

while True:
    connect_with_bluetooth()
