#!/usr/bin/python3
import datetime as dt
import os
import traceback

import requests
import logging
logger = logging.getLogger(__name__)
import json
import datetime as dt
import utilities.connect as connect
import utilities.conversions as conversions
from weather.data import CLIMATE_TYPE_SENSOR_PUSH, Climate

AUTHORIZE_URL = "https://api.sensorpush.com/api/v1/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.sensorpush.com/api/v1/oauth/accesstoken"
DATA_URL = "https://api.sensorpush.com/api/v1/samples"
CALIBRATION_URL = "https://api.sensorpush.com/api/v1/devices/sensors"
TIME_FORMAT_STR = "%Y-%m-%d %H:%M:%S"
CONNECT_ITEM_ID = os.getenv("SENSOR_PUSH_CONNECT_ITEM_ID")
TYPES_PROCESSED = [CLIMATE_TYPE_SENSOR_PUSH]

def check_types(config_data):
    result = config_data.split("|")
    if int(result[0]) and int(result[0]) in TYPES_PROCESSED:
        return True
    if int(result[0]) == 0:
        return True
    return False

def get_sensor_by_key(sensors, key):
    for sensor in sensors:
        if key.startswith(sensor.key):
            return sensor
    return None

def get_authorization():
    try:
        #
        # Get security data
        credentials = connect.get_credentials(CONNECT_ITEM_ID)
        user_name = credentials[0].value
        password = credentials[1].value

        data = {"email": user_name, "password": password}
        json_post_data = json.dumps(data)

        ret = requests.post(AUTHORIZE_URL, data=json_post_data, headers={"Accept": "application/json",
                                                                         "Content-Type": "application/json"})
        if ret.status_code != 200:
            logging.error("Bad response from sensor_push " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from sensor_push. " + str(ret.status_code))
            return

        auth_response = json.loads(ret.content.decode())
        return auth_response["authorization"]

    except Exception as e:
        logging.error("Unable to get sensor_push:authorization " + str(e))
        print(dt.datetime.now().time(), "Unable to get sensor_push:authorization " + str(e))
    return


def get_access_token(authorization_header):
    try:

        data = {"authorization": authorization_header}
        json_post_data = json.dumps(data)

        ret = requests.post(ACCESS_TOKEN_URL, data=json_post_data, headers={"Accept": "application/json",
                                                                            "Content-Type": "application/json"})
        if ret.status_code != 200:
            logging.error("Bad response from sensor_push " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from sensor_push. " + str(ret.status_code))
            return

        auth_response = json.loads(ret.content.decode())
        return auth_response["accesstoken"]

    except Exception as e:
        logging.error("Unable to get sensor_push:accesstoken " + str(e))
        print(dt.datetime.now().time(), "Unable to get sensor_push:accesstoken " + str(e))
    return


def get_sensor_data(access_token, url):
    try:
        data = {"limit": 10}
        json_post_data = json.dumps(data)

        ret = requests.post(url, data=json_post_data, headers={"Accept": "application/json",
                                                               "Authorization": access_token})
        if ret.status_code != 200:
            logging.error("Bad response from sensor_push " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from sensor_push. " + str(ret.status_code))
            raise Exception("Bad response from sensor_push. " + str(ret.status_code))

        response = json.loads(ret.content.decode())
        if not response:
            raise Exception("No Data from SensorPush:SensorData.")

        return response

    except Exception as e:
        logging.error("Unable to get sensor_push:accesstoken " + str(e))
        print(dt.datetime.now().time(), "Unable to get sensor_push:accesstoken " + str(e))
    return


def apply_sensor(climate_sensor, sensor_data, calibration_data, sensor_key):

    try:
        #
        # Time
        time_zone_delta = dt.timedelta(hours=-7)
        time_zone_object = dt.timezone(time_zone_delta, name="MST")
        time_stamp = sensor_data["sensors"][sensor_key][0]["observed"]
        time_stamp = dt.datetime.fromisoformat(time_stamp.replace("Z", "+00:00")).astimezone(time_zone_object)
        climate_sensor.time = time_stamp.strftime(TIME_FORMAT_STR)

        #
        # Temperature
        calibration_temp = calibration_data[sensor_key]["calibration"]["temperature"]
        raw_temp = conversions.get_average(sensor_data["sensors"][sensor_key], "temperature")
        climate_sensor.temperature_calibration = calibration_temp
        climate_sensor.temperature_raw = raw_temp
        climate_sensor.temperature = round(raw_temp + calibration_temp, 2)
        climate_sensor.temperature_c = conversions.f_to_c(climate_sensor.temperature)

        #
        # Humidity
        calibration_humidity = calibration_data[sensor_key]["calibration"]["humidity"]
        raw_humidity = conversions.get_average(sensor_data["sensors"][sensor_key], "humidity")
        climate_sensor.humidity_calibration = calibration_humidity
        climate_sensor.humidity_raw = raw_humidity
        climate_sensor.humidity = round(raw_humidity + calibration_humidity, 2)

    except Exception as e:
        logging.error("Unable to get sensor_push:data " + str(e))
        print(dt.datetime.now().time(), "Unable to get sensor_push:data " + str(e))
    return


def get_weather(home):
    try:

        # get list of objects we care about
        climate_sensors = []

        for key, value in os.environ.items():
            config_data = os.getenv(key)
            if key.startswith("CLIMATE_SENSOR") and check_types(config_data):
                climate_sensors.append(home.climate.create_sensor(config_data))
        if len(climate_sensors) == 0:
            return

        auth_token = get_authorization()
        if not auth_token:
            return
        access_token = get_access_token(auth_token)
        if not access_token:
            return
        calibration_data = get_sensor_data(access_token, CALIBRATION_URL)
        if not calibration_data:
            return
        sensor_data = get_sensor_data(access_token, DATA_URL)
        if not sensor_data:
            return

        for sensor in sensor_data["sensors"]:
            sensor_key = str(sensor)
            climate_sensor = get_sensor_by_key(climate_sensors, sensor_key)
            if climate_sensor:
                apply_sensor(climate_sensor, sensor_data, calibration_data, sensor_key)
                home.climate.sensors.append(climate_sensor)

    except Exception as e:
        traceback.print_exc()
        logging.error(f"Unable to get sensor_push:get_weather {e} ")
        print(dt.datetime.now().time(), "Unable to get sensor_push:get_weather ")
    return
