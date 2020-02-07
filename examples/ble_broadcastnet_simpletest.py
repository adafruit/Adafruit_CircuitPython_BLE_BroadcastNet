"""This is a basic sensor node that uses the internal temperature sensor."""

import adafruit_ble_broadcastnet
import microcontroller
import time

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

last_temperature = None
while True:
    temp = microcontroller.cpu.temperature
    # Round the temperature to the nearest degree to reduce how often it is
    # broadcast.
    temp = round(temp, 0)
    if temp != last_temperature:
        measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
        measurement.temperature = temp
        print(measurement)
        adafruit_ble_broadcastnet.broadcast(measurement)
    last_temperature = temp
    time.sleep(10)
