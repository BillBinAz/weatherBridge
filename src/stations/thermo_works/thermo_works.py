#!/usr/bin/python3
import asyncio
import datetime as dt
import logging
import sys
from dataclasses import asdict

from stations.thermo_works.get_devices_for_user import get_devices_for_user
import utilities.conversions as conversions

HUMIDOR_NODE_ID = 'B0:A7:32:C5:5A:74'
SAFE_NODE_ID = '08:F9:E0:95:B9:20'
KITCHEN_NODE_ID = 'B0:A7:32:CA:4B:F4'
GARAGE_NODE_ID = '10:06:1C:A6:4A:90'

def get_local_value(device_channels, index):
    channel_dict = asdict(device_channels[index])
    local_value = channel_dict['value']
    if not isinstance(local_value, float):
        return -999
    return float(local_value)

def get_weather(weather_data):
    try:
        # asyncio.run(get_devices_for_user(weather_data))
        loop = asyncio.new_event_loop()
        task = loop.create_task(get_devices_for_user())
        loop.run_until_complete(task)
        results = task.result()
        devices = results[0]
        device_channels_by_device = results[1]

        # Print detailed information for each device
        for device in devices:
            assert device.serial is not None
            device_channels = device_channels_by_device.get(device.serial, [])
            local_value = -999

            # SAFE 0: Ambient, 1: Humidity
            if device.device_id == SAFE_NODE_ID:
                local_value = get_local_value(device_channels, 0)
                weather_data.safe.temp  = conversions.format_f(local_value)
                weather_data.safe.temp_c = conversions.f_to_c(local_value)

                local_value = get_local_value(device_channels, 1)
                weather_data.safe.humidity = conversions.format_f(local_value)

            # KITCHEN 0: Ambient, 1: Refrigerator, 2: Freezer
            if device.device_id == KITCHEN_NODE_ID:
                local_value = get_local_value(device_channels, 0)
                weather_data.kitchen.temp  = conversions.format_f(local_value)
                weather_data.kitchen.temp_c = conversions.f_to_c(local_value)

                local_value = get_local_value(device_channels, 1)
                weather_data.kitchen_refrigerator.temp  = conversions.format_f(local_value)
                weather_data.kitchen_refrigerator.temp_c = conversions.f_to_c(local_value)

                local_value = get_local_value(device_channels, 2)
                weather_data.kitchen_freezer.temp  = conversions.format_f(local_value)
                weather_data.kitchen_freezer.temp_c = conversions.f_to_c(local_value)

            # GARAGE 0: Ambient, 1: Freezer
            if device.device_id == GARAGE_NODE_ID:
                local_value = get_local_value(device_channels, 0)
                weather_data.garage.temp  = conversions.format_f(local_value)
                weather_data.garage.temp_c = conversions.f_to_c(local_value)

                local_value = get_local_value(device_channels, 1)
                weather_data.garage_freezer.temp  = conversions.format_f(local_value)
                weather_data.garage_freezer.temp_c = conversions.f_to_c(local_value)

            # HUMIDOR 0: Ambient, 1: Humidity
            if device.device_id == HUMIDOR_NODE_ID:
                local_value = get_local_value(device_channels, 0)
                weather_data.humidor.temp  = conversions.format_f(local_value)
                weather_data.humidor.temp_c = conversions.f_to_c(local_value)

                local_value = get_local_value(device_channels, 1)
                weather_data.humidor.humidity = conversions.format_f(local_value)

    except Exception as e:
        logging.error("Unable to get thermo_works:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get thermo_works:get_weather " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to get thermo_works:get_weather " + str(e))
            print(dt.datetime.now().time(), "Unable to get thermo_works:get_weather " + str(e))
    return