#!/usr/bin/python3

import datetime
import requests
import logging
import json
import sys
from datetime import timedelta

from weather import stations

SECRET_FILE = "./secret/sensor_push"
AUTHORIZE_URL = "https://api.sensorpush.com/api/v1/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.sensorpush.com/api/v1/oauth/accesstoken"
DATA_URL = "https://api.sensorpush.com/api/v1/samples"
CALIBRATION_URL = "https://api.sensorpush.com/api/v1/devices/sensors"
TIME_FORMAT_STR = "%Y-%m-%d %H:%M:%S"
FREEZER_ID = "16838664"
HUMIDOR_ID = "16869529"
MAIN_GARAGE_ID = "16803031"
SAFE_ID = "16866908"

def c_to_f(c_temp):
    #
    # Convert from celsius to fahrenheit
    return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def f_to_c(f_temp):
    #
    # Convert from celsius to fahrenheit
    return round(float(f_temp - 32) * 5.0 / 9.0, 1)


def format_f(value, source):
    #
    # add decimal place
    formatted_value = 0
    try:
        formatted_value = round(float(value) / 10.0, 1)
    except:
        logging.error("Bad Data from sensorPush " + str(value) + " " + source)
        print(datetime.datetime.now().time(), " -  Bad Data from sensorPush " + str(source) + " " + source)
    return formatted_value


def get_authorization():
    try:
        with open(SECRET_FILE, "r") as secret_file:
            user_name = secret_file.readline().strip('\n')
            password = secret_file.readline().strip('\n')

        data = {"email": user_name, "password": password}
        json_post_data = json.dumps(data)

        ret = requests.post(AUTHORIZE_URL, data=json_post_data, headers={"Accept": "application/json",
                                                                         "Content-Type": "application/json"})
        if ret.status_code != 200:
            logging.error("Bad response from sensor_push " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  Bad response from sensor_push. " + str(ret.status_code))
            return

        auth_response = json.loads(ret.content.decode())
        return auth_response["authorization"]

    except Exception as e:
        logging.error("Unable to get sensor_push:authorization " + str(e))
        print(datetime.datetime.now().time(), "Unable to get sensor_push:authorization " + str(e))
    return


def get_access_token(authorization_header):
    try:

        data = {"authorization": authorization_header}
        json_post_data = json.dumps(data)

        ret = requests.post(ACCESS_TOKEN_URL, data=json_post_data, headers={"Accept": "application/json",
                                                                            "Content-Type": "application/json"})
        if ret.status_code != 200:
            logging.error("Bad response from sensor_push " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  Bad response from sensor_push. " + str(ret.status_code))
            return

        auth_response = json.loads(ret.content.decode())
        return auth_response["accesstoken"]

    except Exception as e:
        logging.error("Unable to get sensor_push:accesstoken " + str(e))
        print(datetime.datetime.now().time(), "Unable to get sensor_push:accesstoken " + str(e))
    return


def get_average(data, key):
    how_many = 0
    sum_temp = 0.0
    for sensor in data:
        how_many += 1
        sum_temp += sensor[key]
    if how_many == 0:
        return 0
    return round(float(sum_temp / how_many), 1)


def get_sensor_data(access_token, url):
    try:
        data_to = datetime.datetime.utcnow()
        data_from = data_to - timedelta(minutes=30)
        data = {"limit": 10}
        json_post_data = json.dumps(data)

        ret = requests.post(url, data=json_post_data, headers={"Accept": "application/json",
                                                                    "Authorization": access_token})
        if ret.status_code != 200:
            logging.error("Bad response from sensor_push " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  Bad response from sensor_push. " + str(ret.status_code))
            return

        response = json.loads(ret.content.decode())
        if not response:
            logging.error("No Data from SensorPush:SensorData " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  No Data from SensorPush:SensorData. " + str(ret.status_code))
            return

        return response

    except Exception as e:
        logging.error("Unable to get sensor_push:accesstoken " + str(e))
        print(datetime.datetime.now().time(), "Unable to get sensor_push:accesstoken " + str(e))
    return


def apply_sensor(weather_data_station, sensor_data, calibration_data, sensor_key):

    try:
        #
        # Time
        time_zone_delta = datetime.timedelta(hours=-7)
        time_zone_object = datetime.timezone(time_zone_delta, name="MST")
        time_stamp = sensor_data["sensors"][sensor_key][0]["observed"]
        time_stamp = datetime.datetime.fromisoformat(time_stamp.replace("Z", "+00:00")).astimezone(time_zone_object)
        weather_data_station.time = time_stamp.strftime(TIME_FORMAT_STR)

        #
        # Temperature
        calibration_temp = calibration_data[sensor_key]["calibration"]["temperature"]
        raw_temp = get_average(sensor_data["sensors"][sensor_key], "temperature")
        weather_data_station.temp_calibration = calibration_temp
        weather_data_station.temp_raw = raw_temp
        weather_data_station.temp = round(raw_temp + calibration_temp, 2)
        weather_data_station.temp_c = f_to_c(weather_data_station.temp)

        #
        # Humidity
        calibration_humidity = calibration_data[sensor_key]["calibration"]["humidity"]
        raw_humidity = get_average(sensor_data["sensors"][sensor_key], "humidity")
        weather_data_station.humidity_calibration = calibration_humidity
        weather_data_station.humidity_raw = raw_humidity
        weather_data_station.humidity = round( raw_humidity + calibration_humidity, 2)

    except Exception as e:
        logging.error("Unable to get sensor_push:data " + str(e))
        print(datetime.datetime.now().time(), "Unable to get sensor_push:data " + str(e))
    return


def get_weather(weather_data):
    try:
        time_zone_delta = datetime.timedelta(hours=-7)
        time_zone_object = datetime.timezone(time_zone_delta, name="MST")
        auth_token = get_authorization()
        access_token = get_access_token(auth_token)
        calibration_data = get_sensor_data(access_token, CALIBRATION_URL)
        sensor_data = get_sensor_data(access_token, DATA_URL)

        if sensor_data:
            #
            # Get full keys
            for sensor in sensor_data["sensors"]:
                sensor_key = str(sensor)
                if sensor_key.startswith(HUMIDOR_ID):
                    humidor_key = sensor_key
                elif sensor_key.startswith(MAIN_GARAGE_ID):
                    garage_key = sensor_key
                elif sensor_key.startswith(FREEZER_ID):
                    garage_freezer_key = sensor_key
                elif sensor_key.startswith(SAFE_ID):
                    safe_key = sensor_key
            #
            # Humidor Sensor
            apply_sensor(weather_data.humidor, sensor_data, calibration_data, humidor_key)

            #
            # Freezer Sensor
            apply_sensor(weather_data.main_garage_freezer, sensor_data, calibration_data, garage_freezer_key)

            #
            # Main Garage Sensor
            apply_sensor(weather_data.main_garage, sensor_data, calibration_data, garage_key)

            #
            # Safe Sensor
            apply_sensor(weather_data.safe, sensor_data, calibration_data, safe_key)

    except Exception as e:
        logging.error("Unable to get sensor_push:data " + str(e))
        print(datetime.datetime.now().time(), "Unable to get sensor_push:data " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get sensor_push:data " + str(e))
        print(datetime.datetime.now().time(), "Unable to get sensor_push:data " + str(e))
        return

