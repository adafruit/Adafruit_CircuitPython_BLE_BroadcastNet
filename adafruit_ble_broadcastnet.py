# The MIT License (MIT)
#
# Copyright (c) 2020 Scott Shawcroft for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ble_broadcastnet`
================================================================================

Basic IOT over BLE advertisements.


* Author(s): Scott Shawcroft

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's BLE library: https://github.com/adafruit/Adafruit_CircuitPython_BLE
"""

from adafruit_ble.advertising import Advertisement, LazyObjectField
from adafruit_ble.advertising.standard import ManufacturerData, ManufacturerDataField
import struct

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_BroadcastNet.git"

_MANUFACTURING_DATA_ADT = const(0xff)
_ADAFRUIT_COMPANY_ID = const(0x0822)
_SENSOR_DATA_ID = const(0x0002)

class AdafruitSensorMeasurement(Advertisement):
    """Broadcast a single RGB color."""
    # This prefix matches all
    prefix = struct.pack("<BBH",
                         3,
                         _MANUFACTURING_DATA_ADT,
                         _ADAFRUIT_COMPANY_ID)

    manufacturer_data = LazyObjectField(ManufacturerData,
                                        "manufacturer_data",
                                        advertising_data_type=_MANUFACTURING_DATA_ADT,
                                        company_id=_ADAFRUIT_COMPANY_ID,
                                        key_encoding="<H")

    sequence_number = ManufacturerDataField(0x0003, "<B")
    """Sequence number of the measurement. Used to detect missed packets."""

    acceleration = ManufacturerDataField(0x0a00, "<fff")
    """Acceleration as (x, y, z) tuple of floats in meters per second per second."""

    magnetic = ManufacturerDataField(0x0a01, "<fff")
    """Magnetism as (x, y, z) tuple of floats in micro-Tesla."""

    orientation = ManufacturerDataField(0x0a02, "<fff")
    """Absolution orientation as (x, y, z) tuple of floats in degrees."""

    gyro = ManufacturerDataField(0x0a03, "<fff")
    """Gyro motion as (x, y, z) tuple of floats in radians per second."""

    temperature = ManufacturerDataField(0x0a04, "<f")
    """Temperature as a float in degrees centigrade."""

    eCO2 = ManufacturerDataField(0x0a05, "<f")
    """Equivalent CO2 as a float in parts per million."""

    TVOC = ManufacturerDataField(0x0a06, "<f")
    """Total Volatile Organic Compounds as a float in parts per billion."""

    distance = ManufacturerDataField(0x0a07, "<f")
    """Distance as a float in centimeters."""

    light = ManufacturerDataField(0x0a08, "<f")
    """Brightness as a float without units."""

    lux = ManufacturerDataField(0x0a09, "<f")
    """Brightness as a float in SI lux."""

    pressure = ManufacturerDataField(0x0a0a, "<f")
    """Pressure as a float in hectopascals."""

    relative_humidity = ManufacturerDataField(0x0a0b, "<f")
    """Relative humidity as a float percentage."""

    current = ManufacturerDataField(0x0a0c, "<f")
    """Current as a float in milliamps."""

    voltage = ManufacturerDataField(0x0a0d, "<f")
    """Voltage as a float in Volts."""

    color = ManufacturerDataField(0x0a0e, "<f")
    """Color as RGB integer."""

    # alarm = ManufacturerDataField(0x0a0f, "<f")
    """Alarm as a start date and time and recurrence period. Not supported."""

    # datetime = ManufacturerDataField(0x0a10, "<f")
    """Date and time as a struct. Not supported."""

    duty_cycle = ManufacturerDataField(0x0a11, "<f")
    """16-bit PWM duty cycle. Independent of frequency."""

    frequency = ManufacturerDataField(0x0a12, "<f")
    """As integer Hertz"""

    value = ManufacturerDataField(0x0a13, "<f")
    """16-bit unit-less value. Used for analog values and for booleans."""

    weight = ManufacturerDataField(0x0a14, "<f")
    """Weight as a float in grams."""

    def __init__(self, *, sequence_number=None):
        super().__init__()
        if sequence_number:
            self.sequence_number = sequence_number

    def __str__(self):
        parts = []
        for attr in dir(self.__class__):
            attribute_instance = getattr(self.__class__, attr)
            if issubclass(attribute_instance.__class__, ManufacturerDataField):
                value = getattr(self, attr)
                if value is not None:
                    parts.append("{}={}".format(attr, str(value)))
        return "<{} {} >".format(self.__class__.__name__, " ".join(parts))
