#!/usr/bin/python3

import datetime as dt
import logging

from weather import stations

IOX_INTEGER = 1
GARAGE_FREEZER_TEMP = 14
BACK_YARD_TEMP = 13
MAIN_GARAGE_TEMP = 18
AVERAGE_HOUSE_TEMP = 25
FAN_ZONES_ALL = 9
FAN_ZONES_SOME = 22
ALARM_ALL_ZONES_CLOSED = 12
ENTRY_DOOR_FRONT_CLOSED = 32
ENTRY_DOOR_GARAGE_CLOSED = 33

IOX_STATE = 2
MAIN_GARAGE_STATE = 2
SINGLE_GARAGE_STATE = 1
DOUBLE_GARAGE_STATE = 3
MOTORCYCLE_GARAGE_STATE = 4
IS_RAINING_STATE = 5
ALARM_STATUS_STATE = 7
CONNECT_ITEM_ID = "ymulwralgldqemmer2bx4exr3q"


def main():

    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                            datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)

        #
        # Get weather data from data sources
        weather_data = stations.get_weather()
        print(weather_data)

    except Exception as e:
        logging.error("Unable to update IoX " + str(e))
        print(dt.datetime.now().time(), "Unable to update IoX " + str(e))


main()
