"""This is a basic sensor node that uses the internal temperature sensor and reports it every 10
   seconds."""

import adafruit_ble_broadcastnet
import microcontroller
import time

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

while True:
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()
    measurement.temperature = microcontroller.cpu.temperature
    print(measurement)
    adafruit_ble_broadcastnet.broadcast(measurement)
    time.sleep(10)
