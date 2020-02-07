"""This is a complex sensor node that uses the sensors on a Clue and Feather Bluefruit Sense."""

import board
import adafruit_bmp280
import adafruit_sht31d
import adafruit_apds9960.apds9960
import adafruit_lis3mdl
import adafruit_lsm6ds
import adafruit_ble_broadcastnet
import time

print("This is BroadcastNet sensor:", adafruit_ble_broadcastnet.device_address)

i2c = board.I2C()

# Define sensors:
# Accelerometer/gyroscope:
lsm6ds = adafruit_lsm6ds.LSM6DS33(i2c)

# Magnetometer:
lis3mdl = adafruit_lis3mdl.LIS3MDL(i2c)

# DGesture/proximity/color/light sensor:
# TODO: How do we get the light level?
# apds9960 = adafruit_apds9960.apds9960.APDS9960(i2c)
# apds9960.enable_color = True

# Humidity sensor:
sht31d = adafruit_sht31d.SHT31D(i2c)

# Barometric pressure sensor:
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

last_sht31d_temperature = None
last_sht31d_relative_humidity = None
last_bmp280_temperature = None
last_bmp280_pressure = None
last_lsm6ds_acceleration = None
last_lis3mdl_magnetic = None

while True:
    measurement = adafruit_ble_broadcastnet.AdafruitSensorMeasurement()

    # Handle the two temperature measurements. We must always provide both because they split into
    # feeds based on the position in the field.
    sht31d_temperature = round(sht31d.temperature, 0)
    bmp280_temperature = round(bmp280.temperature, 0)
    if (sht31d_temperature != last_sht31d_temperature or
        bmp280_temperature != last_bmp280_temperature):
        measurement.temperature = (sht31d_temperature, bmp280_temperature)
        last_sht31d_temperature = sht31d_temperature
        last_bmp280_temperature = bmp280_temperature

    # Relative humidity, rounded to the nearest whole integer.
    sht31d_relative_humidity = round(sht31d.relative_humidity, 0)
    if sht31d_relative_humidity != last_sht31d_relative_humidity:
        measurement.relative_humidity = sht31d_relative_humidity
        last_sht31d_relative_humidity = sht31d_relative_humidity

    # Pressure, round to one decimal place.
    bmp280_pressure = round(bmp280.pressure, 1)
    if bmp280_pressure != last_bmp280_pressure:
        measurement.pressure = bmp280_pressure
        last_bmp280_pressure = bmp280_pressure

    # Acceleration, each axis rounded to one decimal place.
    lsm6ds_acceleration = tuple([round(axis, 1) for axis in lsm6ds.acceleration])
    if lsm6ds_acceleration != last_lsm6ds_acceleration:
        measurement.acceleration = lsm6ds_acceleration
        last_lsm6ds_acceleration = lsm6ds_acceleration

    # Magnetic, each axis rounded to two decimal places.
    lis3mdl_magnetic = tuple([round(axis, 2) for axis in lis3mdl.magnetic])
    if lis3mdl_magnetic != last_lis3mdl_magnetic:
        measurement.magnetic = lis3mdl_magnetic
        last_lis3mdl_magnetic = lis3mdl_magnetic

    if measurement:
        print(measurement)
        adafruit_ble_broadcastnet.broadcast(measurement)
    time.sleep(10)
