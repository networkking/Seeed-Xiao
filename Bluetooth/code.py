from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.location_packet import LocationPacket
import time

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
ble.name = "Smart Watch"


increment_counter = 0
running = True
while running:

    # Try to connect
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass # Do this while not connected to a device
        
    while ble.connected:
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, LocationPacket):
                print(f"latitude {packet.latitude}")
                print(f"longitude {packet.longitude}")
                print(f"altitude {packet.altitude}")

    