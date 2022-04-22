#!/usr/bin/python3

import datetime
import requests
import logging
import json
from datetime import timedelta

from weather import stations

SECRET_FILE = "./secret/sensor_push"
AUTHORIZE_URL = "https://api.sensorpush.com/api/v1/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.sensorpush.com/api/v1/oauth/accesstoken"
DATA_URL = "https://api.sensorpush.com/api/v1/samples"
TIME_FORMAT_STR = "%Y-%m-%d %H:%M:%S"
FREEZER_ID = "16838664.5275010362836084938"
HUMIDOR_ID = "16825492.35235396901569655440"


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
        logging.error("Bad Data from isy994 " + str(value) + " " + source)
        print(datetime.datetime.now().time(), " -  Bad Data from isy994 " + str(source) + " " + source)
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


def get_accesstoken(authorization_header):
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


def get_sensor_data(access_token):
    try:
        data_to = datetime.datetime.utcnow()
        data_from = data_to - timedelta(minutes=30)
        data = {"limit": 10}
        json_post_data = json.dumps(data)

        ret = requests.post(DATA_URL, data=json_post_data, headers={"Accept": "application/json",
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


def get_weather(weather_data):
    try:
        time_zone_delta = datetime.timedelta(hours=-7)
        time_zone_object = datetime.timezone(time_zone_delta, name="MST")
        auth_token = get_authorization()
        access_token = get_accesstoken(auth_token)
        sensor_data = get_sensor_data(access_token)

        if sensor_data:
            #
            # Humidor Sensor
            time_stamp = sensor_data["sensors"][HUMIDOR_ID][0]["observed"]
            time_stamp = datetime.datetime.fromisoformat(time_stamp.replace("Z", "+00:00")).astimezone(time_zone_object)

            weather_data.humidor.time = time_stamp.strftime(TIME_FORMAT_STR)
            weather_data.humidor.humidity = get_average(sensor_data["sensors"][HUMIDOR_ID], "humidity")
            weather_data.humidor.temp = get_average(sensor_data["sensors"][HUMIDOR_ID], "temperature")
            weather_data.humidor.temp_c = f_to_c(weather_data.humidor.temp)

            #
            # Freezer Sensor
            time_stamp = sensor_data["sensors"][FREEZER_ID][0]["observed"]
            time_stamp = datetime.datetime.fromisoformat(time_stamp.replace("Z", "+00:00")).astimezone(time_zone_object)

            weather_data.garage_freezer.humidity = get_average(sensor_data["sensors"][FREEZER_ID], "humidity")
            weather_data.garage_freezer.temp = get_average(sensor_data["sensors"][FREEZER_ID], "temperature")
            weather_data.garage_freezer.temp_c = f_to_c(weather_data.garage_freezer.temp)
            weather_data.garage_freezer.time = time_stamp.strftime(TIME_FORMAT_STR)

    except Exception as e:
        logging.error("Unable to get sensor_push:data " + str(e))
        print(datetime.datetime.now().time(), "Unable to get sensor_push:data " + str(e))
        return

