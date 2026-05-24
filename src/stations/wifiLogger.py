#!/usr/bin/python3
import json
import logging
import os
import traceback

import dt
import requests
import tb

import utilities.conversions as conversion_utilities
from weather.data import CLIMATE_TYPE_DAVIS

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
    """Retrieve the last 5 minutes of data from wifiLogger."""
    try:
        response = requests.get(url, verify=False)
        if response.status_code != 200:
            logging.error(f"Bad response from wifilogger: {response.status_code}")
            return None
        return json.loads(response.content.decode())
    except Exception as e:
        logging.error(f"Unable to parse wifilogger: {e}")
        return None


def convert_to_float(value, precision):
    try:
        return round(float(value), precision)
    except ValueError:
        return 0.0


def check_types(config_data):
    """Check if config_data type is in TYPES_PROCESSED."""
    try:
        type_id = int(config_data.split("|")[0])
        return type_id in TYPES_PROCESSED
    except (ValueError, IndexError):
        return False


def get_weather(home):
    """Populate home climate sensor with wifiLogger data."""
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

        # Temperature and humidity
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

        # Spa temperature
        climate_sensor.spa_temp = convert_to_float(wifi_logger_data[SPA_TEMP_ARRAY][SPA_TEMP_INDEX], 2)

        # Pressure
        climate_sensor.pressure = convert_to_float(wifi_logger_data[PRESSURE], 4)

        home.climate.sensors.append(climate_sensor)

    except json.JSONDecodeError as e:
        traceback.print_exc()
        logging.error(f"JSON decode error in wifiLogger: {e} Error occurred on line: {tb[-1][1]}")
        print(dt.datetime.now().time(), "Unable to get wifiLogger:get_weather ")
    except KeyError as e:
        traceback.print_exc()
        logging.error(f"Missing expected key in wifiLogger data: {e} Error occurred on line: {tb[-1][1]}")
        print(dt.datetime.now().time(), "Unable to get wifiLogger:get_weather ")
    except Exception as e:
        traceback.print_exc()
        logging.error(f"Unable to get wifiLogger data: {e} Error occurred on line: {tb[-1][1]}")
        print(dt.datetime.now().time(), "Unable to get wifiLogger:get_weather ")
