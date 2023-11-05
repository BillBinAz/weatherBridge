#!/usr/bin/python3

import datetime

import requests
import logging
import jsonpickle

from weather import data
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
SECRET_FILE = "secret/IoX"


def get_rest():
    try:
        #
        # call home for data
        url = "http://home.evilminions.org/weather/data"
        ret = requests.get(url, verify=False)

        if ret.status_code != 200:
            logging.error(f'Bad response from {url} {str(ret.status_code)}')
            print(datetime.datetime.now().time(), f'Bad response from {url} {str(ret.status_code)}')
            return
        json_content = ret.content.decode()
        return jsonpickle.decode(json_content)
    except Exception as e:
        logging.error(f'Unable to get weather data from home {str(e)}')
        print(datetime.datetime.now().time(), "Unable to get weather data from home " + str(e))
    return


def push_temp_iox(s, user_name, password, variable_type, variable_id, f_temp, label):
    try:
        #
        # Never push defaults to IoX
        if f_temp == data.DEFAULT_TEMP and variable_type == IOX_INTEGER:
            msg = "Default Temp found for " + label + " Type:" + str(variable_type) + " Id:" + str(variable_id)
            logging.error(msg)
            print(datetime.datetime.now().time(), msg)
            return

        push_data_iox(s, user_name, password, variable_type, variable_id, f_temp, label)
    except Exception as e:
        logging.error("Unable to push_temp_iox to IoX " + str(e))
        print(datetime.datetime.now().time(), "Unable to push_temp_iox " + str(e))


def push_data_iox(s, user_name, password, variable_type, variable_id, f_temp, label):
    try:
        #
        # do a get on IoX to update the data
        url = stations.IoX.URL + "/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(
            round(float(f_temp)))
        ret = s.get(url, auth=(user_name, password), verify=False)
        if not str(ret.content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
            logging.error("Failed URL: " + url + " Response: " + str(ret.content))
            print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(ret.content), " ", label)
        else:
            print(datetime.datetime.now().time(), " - Success URL: ", url, " ", label)
    except Exception as e:
        logging.error("Unable to push_data_iox " + str(e))
        print(datetime.datetime.now().time(), "Unable to push_data_iox " + str(e))


def update_iox(weather_dict, s, user_name, password):

    try:
        # temps
        push_temp_iox(s, user_name, password, IOX_INTEGER, BACK_YARD_TEMP, weather_dict["back_yard"]["temp"], 'BACK_YARD_TEMP')
        push_temp_iox(s, user_name, password, IOX_INTEGER, MAIN_GARAGE_TEMP, weather_dict["garage"]["temp"], 'GARAGE_TEMP')
        push_temp_iox(s, user_name, password, IOX_INTEGER, GARAGE_FREEZER_TEMP, weather_dict["main_garage_freezer"]["temp"], ' GARAGE_FREEZER_TEMP')
        push_temp_iox(s, user_name, password, IOX_INTEGER, AVERAGE_HOUSE_TEMP, round(weather_dict["whole_house_fan"]["houseTemp"]), 'AVERAGE_HOUSE_TEMP')

        # alarm status
        push_data_iox(s, user_name, password, IOX_INTEGER, ALARM_ALL_ZONES_CLOSED, weather_dict["alarm"]["all_zones_closed"], ' Alarm: all_zones_closed')
        push_data_iox(s, user_name, password, IOX_INTEGER, FAN_ZONES_ALL, weather_dict["whole_house_fan"]["fan_zones_all"], '  FAN_ZONES_ALL')
        push_data_iox(s, user_name, password, IOX_INTEGER, FAN_ZONES_SOME, weather_dict["whole_house_fan"]["fan_zones_some"], ' FAN_ZONES_SOME')

        # entry doors
        push_data_iox(s, user_name, password, IOX_INTEGER, ENTRY_DOOR_FRONT_CLOSED, weather_dict["alarm"]["front_entry_door"], ' ENTRY_DOOR_FRONT_CLOSED')
        push_data_iox(s, user_name, password, IOX_INTEGER, ENTRY_DOOR_GARAGE_CLOSED, weather_dict["alarm"]["garage_entry_door"], ' ENTRY_DOOR_GARAGE_CLOSED')

        # garage doors
        # push_data_iox(s, user_name, password, IOX_STATE, SINGLE_GARAGE_STATE, weather_dict["alarm"]["single_garage"], '  SINGLE_GARAGE_CLOSED')
        # push_data_iox(s, user_name, password, IOX_STATE, DOUBLE_GARAGE_STATE, weather_dict["alarm"]["double_garage"], '  DOUBLE_GARAGE_CLOSED')

        push_data_iox(s, user_name, password, IOX_STATE, IS_RAINING_STATE, (weather_dict["back_yard"]["rain_rate"] > 0), '  IS_RAINING')
        push_data_iox(s, user_name, password, IOX_STATE, ALARM_STATUS_STATE, (weather_dict["alarm"]["status"]), '  Alarm: Status')
        logging.error("IoX pushed")

    except Exception as e:
        logging.error("Unable to push weather to IoX " + str(e))
        print(datetime.datetime.now().time(), "Unable to push weather to IoX " + str(e))


def main():

    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)

        #
        # Get weather data from data sources
        if __debug__:
            weather_data = stations.get_weather()

        # Get weather data from the rest endpoint
        weather_dict = get_rest()

        #
        # Get IoX security data
        with open(SECRET_FILE, "r") as secret_file:
            user_name = secret_file.readline().strip('\n')
            password = secret_file.readline().strip('\n')

        s = requests.Session()
        update_iox(weather_dict, s, user_name, password)
        s.close()
    except Exception as e:
        logging.error("Unable to update IoX " + str(e))
        print(datetime.datetime.now().time(), "Unable to update IoX " + str(e))


main()
