import time
from adafruit_ble.advertising.standard import ManufacturerDataField
import adafruit_ble
import adafruit_ble_broadcastnet
from secrets import secrets
import sys

if sys.implementation.name == "cpython":
    import requests
else:
    from adafruit_esp32spi import adafruit_esp32spi
    from adafruit_esp32spi import adafruit_esp32spi_wifimanager

    import board
    import busio
    from digitalio import DigitalInOut
    import adafruit_dotstar

    esp32_cs = DigitalInOut(board.D13)
    esp32_ready = DigitalInOut(board.D11)
    esp32_reset = DigitalInOut(board.D12)

    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
    # esp._debug = 1

    status_light = adafruit_dotstar.DotStar(
        board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2
    )
    requests = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(
        esp, secrets, status_light
    )

aio_auth_header = {"X-AIO-KEY": secrets["aio_key"]}
aio_base_url = "https://io.adafruit.com/api/v2/" + secrets["aio_username"]


def aio_post(path, **kwargs):
    kwargs["headers"] = aio_auth_header
    return requests.post(aio_base_url + path, **kwargs)


def aio_get(path, **kwargs):
    kwargs["headers"] = aio_auth_header
    return requests.get(aio_base_url + path, **kwargs)


def create_group(name):
    response = aio_post("/groups", json={"name": name})
    if response.status_code != 201:
        print(name)
        print(response.content)
        print(response.status_code)
        raise RuntimeError("unable to create new group")
    return response.json()["key"]


def create_feed(group_key, name):
    response = aio_post(
        "/groups/{}/feeds".format(group_key), json={"feed": {"name": name}}
    )
    if response.status_code != 201:
        print(name)
        print(response.content)
        print(response.status_code)
        raise RuntimeError("unable to create new feed")
    return response.json()["key"]


def create_data(group_key, data):
    response = aio_post("/groups/{}/data".format(group_key), json={"feeds": data})
    if response.status_code == 429:
        print("Throttled!")
        return False
    if response.status_code != 200:
        print(response.status_code, response.json())
        raise RuntimeError("unable to create new data")
    response.close()
    return True


def convert_to_feed_data(values, attribute_name, attribute_instance):
    feed_data = []
    # Wrap single value entries for enumeration.
    if not isinstance(values, tuple) or (
        attribute_instance.element_count > 1 and not isinstance(values[0], tuple)
    ):
        values = (values,)
    for i, value in enumerate(values):
        key = attribute_name.replace("_", "-") + "-" + str(i)
        if isinstance(value, tuple):
            for j in range(attribute_instance.element_count):
                feed_data.append(
                    {
                        "key": key + "-" + attribute_instance.field_names[j],
                        "value": value[j],
                    }
                )
        else:
            feed_data.append({"key": key, "value": value})
    return feed_data


ble = adafruit_ble.BLERadio()
address = ble._adapter.address
bridge_address = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*address.address_bytes)
print("This is BroadcastNet bridge:", bridge_address)
print()

print("Fetching existing feeds.")

existing_feeds = {}
response = aio_get("/groups")
for group in response.json():
    if "-" not in group["key"]:
        continue
    pieces = group["key"].split("-")
    if len(pieces) != 4 or pieces[0] != "bridge" or pieces[2] != "sensor":
        continue
    _, bridge, _, sensor_address = pieces
    if bridge != bridge_address:
        continue
    existing_feeds[sensor_address] = []
    for feed in group["feeds"]:
        feed_key = feed["key"].split(".")[-1]
        existing_feeds[sensor_address].append(feed_key)

print(existing_feeds)

print("scanning")
print()
sequence_numbers = {}
# By providing Advertisement as well we include everything, not just specific advertisements.
for measurement in ble.start_scan(
    adafruit_ble_broadcastnet.AdafruitSensorMeasurement, interval=0.5
):
    reversed_address = [measurement.address.address_bytes[i] for i in range(5, -1, -1)]
    sensor_address = "{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(*reversed_address)
    if sensor_address not in sequence_numbers:
        sequence_numbers[sensor_address] = measurement.sequence_number - 1 % 256
    # Skip if we are getting the same broadcast more than once.
    if measurement.sequence_number == sequence_numbers[sensor_address]:
        continue
    # print(sensor_address, measurement, measurement.sequence_number, sequence_numbers[sensor_address])
    number_missed = measurement.sequence_number - sequence_numbers[sensor_address] - 1
    if number_missed < 0:
        number_missed += 256
    group_key = "bridge-{}-sensor-{}".format(bridge_address, sensor_address)
    if sensor_address not in existing_feeds:
        create_group("Bridge {} Sensor {}".format(bridge_address, sensor_address))
        create_feed(group_key, "Missed Message Count")
        existing_feeds[sensor_address] = ["missed-message-count"]

    data = [{"key": "missed-message-count", "value": number_missed}]
    for attribute in dir(measurement.__class__):
        attribute_instance = getattr(measurement.__class__, attribute)
        if issubclass(attribute_instance.__class__, ManufacturerDataField):
            if attribute != "sequence_number":
                values = getattr(measurement, attribute)
                if values is not None:
                    data.extend(
                        convert_to_feed_data(values, attribute, attribute_instance)
                    )

    for feed_data in data:
        if feed_data["key"] not in existing_feeds[sensor_address]:
            create_feed(group_key, feed_data["key"])
            existing_feeds[sensor_address].append(feed_data["key"])

    start_time = time.monotonic()
    print(group_key, data)
    # Only update the previous sequence if we logged successfully.
    if create_data(group_key, data):
        sequence_numbers[sensor_address] = measurement.sequence_number

    duration = time.monotonic() - start_time
    print("Done logging measurement to IO. Took {} seconds".format(duration))
    print()

print("scan done")
