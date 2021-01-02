"""This example merely scans for broadcastnet packets as a quick check that something is sending them."""

from adafruit_ble.advertising.standard import ManufacturerDataField
import adafruit_ble
import adafruit_ble_broadcastnet

ble = adafruit_ble.BLERadio()

print("scanning")
# By providing Advertisement as well we include everything, not just specific advertisements.
for advert in ble.start_scan(
    adafruit_ble_broadcastnet.AdafruitSensorMeasurement, interval=0.5
):
    print(advert)