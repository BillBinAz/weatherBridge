#!/usr/bin/python3
import datetime as dt
import os

import requests
import logging
import json
import utilities.connect as connect
import re
import functools

CONNECT_ITEM_ID = os.getenv("HOME_ASSISTANT_CONNECT_ITEM_ID")
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL")

def get_bearer_token():
    try:
        #
        # Get security data
        credentials = connect.get_credentials(CONNECT_ITEM_ID)
        return credentials[0].value

    except Exception as e:
        logging.error("Unable to get home-assistant:get_bearer_token " + str(e))
        print(dt.datetime.now().time(), "Unable to home-assistant:get_bearer_token " + str(e))
    return


def get_sensor_data(bearer_token, key, s):
    url = HOME_ASSISTANT_URL + key
    try:
        ret = s.get(url, headers={"Accept": "application/json", "Authorization": "Bearer " + bearer_token})

        if ret.status_code != 200:
            logging.error("Bad response from home-assistant " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from home-assistant. " + str(ret.status_code))
            raise Exception("Bad response from home-assistant " + str(ret.status_code))

        response = json.loads(ret.content.decode())
        if not response:
            raise Exception("No Data from home-assistant:SensorData.")

        return response

    except Exception as e:
        logging.error("Unable to get home-assistant:get_sensor_data Key: " + key + " " + str(e))
        print(dt.datetime.now().time(), "Unable to get home-assistant:get_sensor_data " + url + str(e))
    return


def get_temperature(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    return sensor_data["state"]


def get_occupancy(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] == "on":
        return 1
    else:
        return 0


def get_garage_door(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] == "off":
        return 1
    else:
        return 0


def get_on_off_state(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] == "off":
        return 1
    else:
        return 0


def get_alarm_label(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return ""
    label = sensor_data["state"]

    if re.search('fault', label, re.IGNORECASE):
        return "Not Ready"

    label = label.replace("*", "")
    return label[:10].title().strip()


def get_alarm_status(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] != "disarmed":
        return 1
    else:
        return 0


def get_thermostat_data(weather_data, key, object_path, bearer_token, s):


    sensor_data = get_sensor_data(bearer_token, key, s)

    path = object_path + ".heat_set"
    set_nested_attr(weather_data, path, sensor_data["attributes"]["target_temp_high"])

    path = object_path + ".cool_set"
    set_nested_attr(weather_data, path, sensor_data["attributes"]["target_temp_low"])

    path = object_path + ".humidity"
    set_nested_attr(weather_data, path, sensor_data["attributes"]["current_humidity"])

    path = object_path + ".fan"
    set_nested_attr(weather_data, path, sensor_data["attributes"]["fan_mode"][:10].title().strip())

    path = object_path + ".temp"
    set_nested_attr(weather_data, path, sensor_data["attributes"]["current_temperature"])

    path = object_path + ".state"
    set_nested_attr(weather_data, path, sensor_data["attributes"]["hvac_action"][:10].title().strip())

    mode = sensor_data["attributes"]["preset_mode"]
    path = object_path + ".mode"
    if sensor_data is None:
        return
    if sensor_data["state"] == "off":
        set_nested_attr(weather_data, path, "Off")
    elif mode == "temp":
        set_nested_attr(weather_data, path, "Override")
    else:
        set_nested_attr(weather_data, path, mode[:10].title().strip())


def set_nested_attr(obj, delimited_str, value, delimiter='.'):
    """
    Traverses an object dynamically using a delimited string
    and sets the value of the final attribute.
    """
    attributes = delimited_str.split(delimiter)

    # Get the parent object of the target attribute
    parent_obj = functools.reduce(getattr, attributes[:-1], obj)

    # Set the new value on the target attribute
    setattr(parent_obj, attributes[-1], value)


def get_weather(weather_data):

    s = requests.Session()

    try:
        bearer_token = get_bearer_token()
        if not bearer_token:
            raise Exception("No Data from home-assistant:BearerToken.")
        #

        for key, value in os.environ.items():
            if key.endswith("_SRC"):
                dest_key = key.replace("_SRC", "_DEST")
                id_from_key = os.getenv(key)

                if not id_from_key:
                    raise Exception("ID not found from key: " + key + " from home-assistant:weather_data.")

                object_path = os.getenv(dest_key)
                if not object_path:
                    raise Exception("object_path not found from key: " + dest_key + " from home-assistant:weather_data.")

                if  "THERMOSTAT" in key:
                    get_thermostat_data(weather_data, id_from_key, object_path, bearer_token, s)
                elif "OCCUPANCY_SRC" in key:
                    set_nested_attr(weather_data, object_path, get_occupancy(bearer_token, id_from_key, s))
                elif "TEMPERATURE_SRC" in key or "HUMIDITY_SRC" in key:
                    set_nested_attr(weather_data, object_path, get_temperature(bearer_token, id_from_key, s))
                elif "ALARM_STATUS_LABEL" in key:
                    set_nested_attr(weather_data, object_path, get_alarm_label(bearer_token, id_from_key, s))
                elif "ALARM_STATUS" in key:
                    set_nested_attr(weather_data, object_path, get_alarm_status(bearer_token, id_from_key, s))
                else:
                    set_nested_attr(weather_data, object_path, get_on_off_state(bearer_token, id_from_key, s))


    except Exception as e:
        logging.error("Unable to get home-assistant:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get home-assistant:get_weather " + str(e))
    finally:
        s.close()
    return
