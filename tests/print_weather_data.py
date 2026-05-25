#!/usr/bin/python3

import datetime as dt
import json
import logging

from weather import stations, data


def main():
    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                            datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)
        #
        # Get weather data from data sources
        weather_data = stations.get_weather()
        print(weather_data.to_json())
    except Exception as e:
        logging.error("Unable to update Home" + str(e))
        print(dt.datetime.now().time(), "Unable to update Home " + str(e))


main()
