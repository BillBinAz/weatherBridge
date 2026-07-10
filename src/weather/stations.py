#!/usr/bin/python3
import os
import sys
import traceback
from stations import wifiLogger, home_assistant, sensorPush
from weather import data
from stations.thermo_works import thermo_works
import datetime as dt
import logging

def get_weather():
    home = data.Home()

    try:
        # Configure logging
        log_file = os.environ.get('LOG_FILE', 'weather_bridge_rest.log')
        logging.basicConfig(
            filename=log_file,
            format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO
        )
        home_assistant.get_weather(home)
        wifiLogger.get_weather(home)
        thermo_works.get_weather(home)
        sensorPush.get_weather(home)

    except Exception as e:
        traceback.print_exc()
        exc_info = sys.exc_info()
        line_number = exc_info[2].tb_lineno if exc_info[2] else "unknown"
        logging.error(f"Unable to get station data: {e} Error occurred on line: {line_number}")
        print(dt.datetime.now().time(), "Unable to get get station:get_weather ")
    return home

