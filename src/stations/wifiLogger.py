#!/usr/bin/python3

import datetime as dt
import json
import requests
import logging
import sys
import utilities.conversions as conversion_utilities

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
SPA_TEMP_ARRAY = 'hlxlt0'
SPA_TEMP_INDEX = 1


def get_data():
    #
    # get the last 5 minutes worth of data
    url = "http://wifilogger.evilminions.org/wflexp.json"
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


def get_weather(weather_data):

    try:
        wifi_logger_data = get_data()

        # Temperature - Back yard
        weather_data.back_yard.temp = convert_to_float(wifi_logger_data[TEMPERATURE_OUTDOOR], 2)
        weather_data.back_yard.humidity = convert_to_float(wifi_logger_data[HUMIDITY_OUTDOOR], 2)
        weather_data.back_yard.dew_point = convert_to_float(wifi_logger_data[DEP_POINT], 2)

        # Rain
        weather_data.back_yard.rain_rate = convert_to_float(wifi_logger_data[RAIN_RATE], 2)
        weather_data.back_yard.rain_total = convert_to_float(wifi_logger_data[RAIN_24_HOURS], 2)

        # Wind
        weather_data.back_yard.wind_speed = convert_to_float(wifi_logger_data[WIND_SPEED], 2)
        weather_data.back_yard.wind_gust = convert_to_float(wifi_logger_data[WIND_GUST], 2)
        weather_data.back_yard.wind_direction = conversion_utilities.deg_to_compass(wifi_logger_data[WIND_DIRECTION])
        weather_data.back_yard.wind_chill = convert_to_float(wifi_logger_data[WIND_CHILL], 2)

        # spa
        weather_data.back_yard.spa_temp = convert_to_float(wifi_logger_data[SPA_TEMP_ARRAY][SPA_TEMP_INDEX], 2)

        # Pressure
        weather_data.back_yard.pressure = convert_to_float(wifi_logger_data[PRESSURE], 4)

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
