#!/usr/bin/python3
import traceback
from stations import wifiLogger, home_assistant, sensorPush
from weather import data
from stations.thermo_works import thermo_works
import datetime as dt
import logging
import utilities.conversions as conv


def get_weather():
    cur_weather = data.Home()

    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

        home_assistant.get_weather(cur_weather)
        wifiLogger.get_weather(cur_weather)
        thermo_works.get_weather(cur_weather)
        sensorPush.get_weather(cur_weather)

    except Exception as e:
        traceback.print_exc()
        logging.error(f"Unable to get wifiLogger data: {e} Error occurred on line: {traceback[-1][1]}")
        print(dt.datetime.now().time(), "Unable to get get station:get_weather ")
    return cur_weather
