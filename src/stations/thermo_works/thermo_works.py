#!/usr/bin/python3
import asyncio
import datetime as dt
import logging
logger = logging.getLogger(__name__)
import os
import traceback
from stations.thermo_works.get_devices_for_user import get_devices_for_user
import utilities.conversions as conversions
from weather.data import CLIMATE_TYPE_THERMOWORKS_NODE, CLIMATE_TYPE_THERMOWORKS_NODE_WITH_HUMIDITY, CLIMATE_TYPE_THERMOWORKS_NODE_TWO_CHANNEL

TYPES_PROCESSED = [CLIMATE_TYPE_THERMOWORKS_NODE, CLIMATE_TYPE_THERMOWORKS_NODE_WITH_HUMIDITY, CLIMATE_TYPE_THERMOWORKS_NODE_TWO_CHANNEL]

def check_types(config_data):
    try:
        result = config_data.split("|")
        type_id = int(result[0])
        if type_id and type_id in TYPES_PROCESSED:
            return True
        if type_id == 0:
            return True

        return False
    except (ValueError, IndexError, AttributeError):
        return False

def get_sensor_by_key(sensors, key):
    for sensor in sensors:
        if sensor.key == key:
            return sensor
    return None

def get_weather(home):
    try:
        # get list of objects we care about
        sensors = []

        for key, value in os.environ.items():
            config_data = os.getenv(key)
            if key.startswith("CLIMATE_SENSOR") and check_types(config_data):
                sensors.append(home.climate.create_sensor(config_data))
        if len(sensors) == 0:
            return

        # asyncio.run(get_devices_for_user(home))
        loop = asyncio.new_event_loop()
        task = loop.create_task(get_devices_for_user())
        loop.run_until_complete(task)
        results = task.result()
        devices = results[0]
        device_channels_by_device = results[1]

        for device in devices:
            try:
                if not device.serial:
                    continue

                device_channels = device_channels_by_device.get(device.serial, [])

                if not device.device_id:
                    continue

                sensor = get_sensor_by_key(sensors, device.device_id)
                if sensor is not None:
                    if sensor.type == CLIMATE_TYPE_THERMOWORKS_NODE_WITH_HUMIDITY:
                        # 0: Ambient, 1: Humidity
                        if device_channels[0].value is not None:
                            sensor.temperature = conversions.format_f(device_channels[0].value)

                        if device_channels[1].value is not None:
                            sensor.humidity = conversions.format_f(device_channels[1].value)
                        home.climate.sensors.append(sensor)
                    elif sensor.type == CLIMATE_TYPE_THERMOWORKS_NODE_TWO_CHANNEL:
                        # 0: Ambient, 1: Refrigerator, 2: Freezer
                        if device_channels[0].value is not None:
                            sensor.temperature = conversions.format_f(device_channels[0].value)

                        if device_channels[1].value is not None:
                            sensor.temperature_probe_0 = conversions.format_f(device_channels[1].value)

                        if device_channels[2].value is not None:
                            sensor.temperature_probe_1 = conversions.format_f(device_channels[2].value)
                        home.climate.sensors.append(sensor)
                    elif sensor.type == CLIMATE_TYPE_THERMOWORKS_NODE:
                        # 0: Ambient, 1: Freezer
                        if device_channels[0].value is not None:
                            sensor.temperature = conversions.format_f(device_channels[0].value)

                        if device_channels[1].value is not None:
                            sensor.temperature_probe_0 = conversions.format_f(device_channels[1].value)
                        home.climate.sensors.append(sensor)
            except Exception as e:
                traceback.print_exc()
                logging.error(f"Unable to get thermo_works:device {device.serial} {e}")
                print(dt.datetime.now().time(), f"Unable to get thermo_works:get_weather {e}")

    except Exception as e:
        traceback.print_exc()
        logging.error(f"Unable to get thermo_works:get_weather {e}")
        print(dt.datetime.now().time(), f"Unable to get thermo_works:get_weather {e}")
    return