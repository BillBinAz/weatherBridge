#!/usr/bin/python3
import datetime as dt
import requests
import logging
import json
import sys
import utilities.connect as connect
import utilities.conversions as conversions

SECRET_FILE = "./secret/sensor_push"
AUTHORIZE_URL = "https://api.sensorpush.com/api/v1/oauth/authorize"
ACCESS_TOKEN_URL = "https://api.sensorpush.com/api/v1/oauth/accesstoken"
DATA_URL = "https://api.sensorpush.com/api/v1/samples"
CALIBRATION_URL = "https://api.sensorpush.com/api/v1/devices/sensors"
TIME_FORMAT_STR = "%Y-%m-%d %H:%M:%S"
FREEZER_ID = "16838664"
HUMIDOR_ID = "16869529"
GARAGE_ID = "16803031"
SAFE_ID = "16866908"
SERVER_RACK = "16867526"
CONNECT_ITEM_ID = "axpjey2v3x2szvumkjukz2w5m4"


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


def apply_sensor(weather_data_station, sensor_data, calibration_data, sensor_key):

    try:
        #
        # Time
        time_zone_delta = dt.timedelta(hours=-7)
        time_zone_object = dt.timezone(time_zone_delta, name="MST")
        time_stamp = sensor_data["sensors"][sensor_key][0]["observed"]
        time_stamp = dt.datetime.fromisoformat(time_stamp.replace("Z", "+00:00")).astimezone(time_zone_object)
        weather_data_station.time = time_stamp.strftime(TIME_FORMAT_STR)

        #
        # Temperature
        calibration_temp = calibration_data[sensor_key]["calibration"]["temperature"]
        raw_temp = conversions.get_average(sensor_data["sensors"][sensor_key], "temperature")
        weather_data_station.temp_calibration = calibration_temp
        weather_data_station.temp_raw = raw_temp
        weather_data_station.temp = round(raw_temp + calibration_temp, 2)
        weather_data_station.temp_c = conversions.f_to_c(weather_data_station.temp)

        #
        # Humidity
        calibration_humidity = calibration_data[sensor_key]["calibration"]["humidity"]
        raw_humidity = conversions.get_average(sensor_data["sensors"][sensor_key], "humidity")
        weather_data_station.humidity_calibration = calibration_humidity
        weather_data_station.humidity_raw = raw_humidity
        weather_data_station.humidity = round(raw_humidity + calibration_humidity, 2)

    except Exception as e:
        logging.error("Unable to get sensor_push:data " + str(e))
        print(dt.datetime.now().time(), "Unable to get sensor_push:data " + str(e))
    return


def get_weather(weather_data):
    try:
        auth_token = get_authorization()
        access_token = get_access_token(auth_token)
        calibration_data = get_sensor_data(access_token, CALIBRATION_URL)
        sensor_data = get_sensor_data(access_token, DATA_URL)

        if sensor_data:
            #
            # Get full keys
            humidor_key = 0
            garage_key = 0
            garage_freezer_key = 0
            server_rack_key = 0
            safe_key = 0

            for sensor in sensor_data["sensors"]:
                sensor_key = str(sensor)
                if sensor_key.startswith(HUMIDOR_ID):
                    humidor_key = sensor_key
                elif sensor_key.startswith(GARAGE_ID):
                    garage_key = sensor_key
                elif sensor_key.startswith(FREEZER_ID):
                    garage_freezer_key = sensor_key
                elif sensor_key.startswith(SAFE_ID):
                    safe_key = sensor_key
                elif sensor_key.startswith(SERVER_RACK):
                    server_rack_key = sensor_key
            #
            # Humidor Sensor
            #  apply_sensor(weather_data.humidor, sensor_data, calibration_data, humidor_key)

            #
            # Freezer Sensor
            apply_sensor(weather_data.main_garage_freezer, sensor_data, calibration_data, garage_freezer_key)

            #
            # Garage Sensor
            apply_sensor(weather_data.garage, sensor_data, calibration_data, garage_key)

            #
            # Rack Sensor
            apply_sensor(weather_data.rack, sensor_data, calibration_data, server_rack_key)

            #
            # Safe Sensor
            # apply_sensor(weather_data.safe, sensor_data, calibration_data, safe_key)

    except Exception as e:
        logging.error("Unable to get sensor_push:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get sensor_push:get_weather " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to get sensor_push:get_weather " + str(e))
            print(dt.datetime.now().time(), "Unable to get sensor_push:get_weather " + str(e))
    return
