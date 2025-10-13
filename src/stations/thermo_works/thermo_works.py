#!/usr/bin/python3
import asyncio
import datetime as dt
import logging
import sys

from stations.thermo_works.get_devices_for_user import get_devices_for_user


def get_weather(weather_data):
    try:
        asyncio.run(get_devices_for_user(weather_data))



    except Exception as e:
        logging.error("Unable to get sensor_push:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get sensor_push:get_weather " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to get sensor_push:get_weather " + str(e))
            print(dt.datetime.now().time(), "Unable to get sensor_push:get_weather " + str(e))
    return