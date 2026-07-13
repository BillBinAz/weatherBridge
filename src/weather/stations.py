#!/usr/bin/python3
import os
import sys
import traceback
from stations import wifiLogger, home_assistant, sensorPush
from weather import data
from stations.thermo_works import thermo_works
import datetime as dt
import logging

def _collect_station(home, collector, name):
    try:
        collector(home)
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Unable to get station data from {name}: {e}")
        print(dt.datetime.now().time(), f"Unable to get station data from {name}")


def get_weather():
    home = data.Home()

    # Configure logging
    log_file = os.environ.get('LOG_FILE', 'weather_bridge_rest.log')
    logging.basicConfig(
        filename=log_file,
        format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    _collect_station(home, home_assistant.get_weather, "home_assistant")
    _collect_station(home, wifiLogger.get_weather, "wifiLogger")
    _collect_station(home, thermo_works.get_weather, "thermo_works")
    _collect_station(home, sensorPush.get_weather, "sensorPush")
    return home
