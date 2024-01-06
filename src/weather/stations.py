#!/usr/bin/python3
from stations import wifiLogger, home_assistant, sensorPush
from weather import data
import datetime as dt
import logging
import sys
import utilities.conversions as conv


def get_weather():
    cur_weather = data.WeatherData()

    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                            datefmt='%Y-%m-%d,%H:%M:%S:%f', level=logging.INFO)

        cur_weather = data.WeatherData()
        home_assistant.get_weather(cur_weather)
        wifiLogger.get_weather(cur_weather)
        sensorPush.get_weather(cur_weather)

        # calculate average house temp
        cur_weather.whole_house_fan.average_house_temp \
            = conv.get_average_from_list([cur_weather.bedroom_left.temp,
                                          cur_weather.bedroom_right.temp,
                                          cur_weather.hallway_thermostat.sensor.temp,
                                          cur_weather.living_room.temp,
                                          cur_weather.master_bedroom.temp,
                                          cur_weather.office.temp])

    except Exception as e:
        logging.error("Unable to get station:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get station:get_weather " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get station:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get station:get_weather " + str(e))

    return cur_weather
