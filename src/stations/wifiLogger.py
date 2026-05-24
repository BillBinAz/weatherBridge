#!/usr/bin/python3

import datetime as dt
import json
import os

import requests
import logging
import sys
import utilities.conversions as conversion_utilities
from weather.data import Climate, CLIMATE_TYPE_DAVIS

TYPES_PROCESSED = [CLIMATE_TYPE_DAVIS]
S_OK = 200
TEMPERATURE_OUTDOOR = 'tempout'
LEAF_TEMP = 'xlt'
HUMIDITY_OUTDOOR = 'humout'
DEP_POINT = 'dew'
RAIN_RATE = 'rainr'
RAIN_24_HOURS = 'rain24'
WIND_DIRECTION = 'winddir'
WIND_GUST = 'gust'
WIND_SPEED = 'windspd'
WIND_CHILL = 'chill'
PRESSURE = 'bar'
SPA_TEMP_ARRAY = 'xlt'
SPA_TEMP_INDEX = 0


def get_data(url):
    #
    # get the last 5 minutes worth of data
    try:
        #
        # Pull the data
        ret = requests.get(url, verify=False)
        ret.close()
        if ret.status_code != 200:
            logging.error("Bad response from wifilogger " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from wifilogger. " + str(ret.status_code))
        return json.loads(ret.content.decode())
    except Exception as e:
        logging.error("Unable to parse wifilogger " + str(e))
        print(dt.datetime.now().time(), "Unable to parse wifilogger " + str(e))
    return


def convert_to_float(value, precision):
    try:
        return round(float(value), precision)
    except ValueError:
        return 0.0


def check_types(config_data):
    for key, value in os.environ.items():
        result = config_data.split("|")
        if int(result[0]) and int(result[0]) in TYPES_PROCESSED:
            return True
    return False


def get_weather(home):

    try:
        found = False
        for key, value in os.environ.items():
            config_data = os.getenv(key)
            if key.startswith("CLIMATE_SENSOR") and check_types(config_data):
                found = True
                break

        if not found:
            return

        climate_sensor = home.climate.create_sensor(config_data)
        wifi_logger_data = get_data(climate_sensor.url)

        if not wifi_logger_data:
            return

        # Temperature - Back yard
        climate_sensor.temperature = convert_to_float(wifi_logger_data[TEMPERATURE_OUTDOOR], 2)
        climate_sensor.humidity = convert_to_float(wifi_logger_data[HUMIDITY_OUTDOOR], 2)
        climate_sensor.dew_point = convert_to_float(wifi_logger_data[DEP_POINT], 2)

        # Rain
        climate_sensor.rain_rate = convert_to_float(wifi_logger_data[RAIN_RATE], 2)
        climate_sensor.rain_total = convert_to_float(wifi_logger_data[RAIN_24_HOURS], 2)

        # Wind
        climate_sensor.wind_speed = convert_to_float(wifi_logger_data[WIND_SPEED], 2)
        climate_sensor.wind_gust = convert_to_float(wifi_logger_data[WIND_GUST], 2)
        climate_sensor.wind_direction = conversion_utilities.deg_to_compass(wifi_logger_data[WIND_DIRECTION])
        climate_sensor.wind_chill = convert_to_float(wifi_logger_data[WIND_CHILL], 2)

        # spa
        climate_sensor.spa_temp = convert_to_float(wifi_logger_data[SPA_TEMP_ARRAY][SPA_TEMP_INDEX], 2)

        # Pressure
        climate_sensor.pressure = convert_to_float(wifi_logger_data[PRESSURE], 4)

        home.climate.sensors.append(climate_sensor)

    except json.JSONDecodeError as e:
        logging.error("Unable to parse wifi_logger_data:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to parse wifi_logger_data:get_weather " + str(e))
    except Exception as e:
        logging.error("Unable to parse wifi_logger_data: get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to parse wifi_logger_data: get_weather " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get wifi_logger_data:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get wifi_logger_data:get_weather " + str(e))
    return
