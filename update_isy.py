#!/usr/bin/python3

import datetime

import requests
import logging
import jsonpickle

from weather import data
from weather import stations

ISY_INTEGER = 1
GARAGE_FREEZER_TEMP = 14
BACK_YARD_TEMP = 13
MAIN_GARAGE_TEMP = 18
AVERAGE_HOUSE_TEMP = 25
FAN_ZONES_ALL = 9
FAN_ZONES_SOME = 22

ISY_STATE = 2
MAIN_GARAGE_STATE = 2
BIKE_GARAGE_STATE = 3
MOTORCYCLE_GARAGE_STATE = 4
IS_RAINING_STATE = 5
SECRET_FILE = "secret/isy994"


def get_rest():
    try:
        #
        # call home for data
        url = "https://home.evilminions.org/weather/data"
        ret = requests.get(url, verify=False)

        if ret.status_code != 200:
            logging.error("Bad response from isy994 " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  Bad response from isy994. " + str(ret.status_code))
            return
        json_content = ret.content.decode()
        return jsonpickle.decode(json_content)
    except Exception as e:
        logging.error("Unable to get weather data from home " + str(e))
        print(datetime.datetime.now().time(), "Unable to get weather data from home " + str(e))
    return


def push_temp_isy(s, user_name, password, variable_type, variable_id, f_temp, label):
    #
    # Never push defaults to ISY
    if f_temp == data.DEFAULT_TEMP and variable_type == ISY_INTEGER:
        msg = "Default Temp found for " + label + " Type:" + str(variable_type) + " Id:" + str(variable_id)
        logging.error(msg)
        print(datetime.datetime.now().time(), msg)
        return

    push_data_isy(s, user_name, password, variable_type, variable_id, f_temp, label)


def push_data_isy(s, user_name, password, variable_type, variable_id, f_temp, label):
    #
    # do a get on isy994 to update the data
    url = stations.isy994.ISY_URL + "/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(
        round(float(f_temp)))
    ret = s.get(url, auth=(user_name, password), verify=False)
    if not str(ret.content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
        logging.error("Failed URL: " + url + " Response: " + str(ret.content))
        print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(ret.content), " ", label)
    else:
        print(datetime.datetime.now().time(), " - Success URL: ", url, " ", label)


def update_isy(weather_dict, s, user_name, password):

    try:
        # temps
        push_temp_isy(s, user_name, password, ISY_INTEGER, BACK_YARD_TEMP, weather_dict["back_yard"]["temp"], 'BACK_YARD_TEMP')
        push_temp_isy(s, user_name, password, ISY_INTEGER, MAIN_GARAGE_TEMP, weather_dict["main_garage"]["temp"], 'MAIN_GARAGE_TEMP')
        push_temp_isy(s, user_name, password, ISY_INTEGER, GARAGE_FREEZER_TEMP, weather_dict["main_garage_freezer"]["temp"], ' GARAGE_FREEZER_TEMP')
        push_temp_isy(s, user_name, password, ISY_INTEGER, AVERAGE_HOUSE_TEMP, round(weather_dict["whole_house_fan"]["houseTemp"]), 'AVERAGE_HOUSE_TEMP')

        # alarm status
        push_data_isy(s, user_name, password, ISY_INTEGER, FAN_ZONES_ALL, weather_dict["whole_house_fan"]["fan_zones_all"], '  FAN_ZONES_ALL')
        push_data_isy(s, user_name, password, ISY_INTEGER, FAN_ZONES_SOME, weather_dict["whole_house_fan"]["fan_zones_some"], ' FAN_ZONES_SOME')

        # garage doors
        push_data_isy(s, user_name, password, ISY_STATE, BIKE_GARAGE_STATE, weather_dict["alarm"]["bike_garage"], '  BIKE_GARAGE_CLOSED')
        push_data_isy(s, user_name, password, ISY_STATE, MOTORCYCLE_GARAGE_STATE, weather_dict["alarm"]["mc_garage"], '  MC_GARAGE_CLOSED')
        push_data_isy(s, user_name, password, ISY_STATE, MAIN_GARAGE_STATE, weather_dict["alarm"]["main_garage"], '  MAIN_GARAGE_CLOSED')
        push_data_isy(s, user_name, password, ISY_STATE, IS_RAINING_STATE, (weather_dict["back_yard"]["rain_rate"] > 0), '  IS_RAINING')
        logging.error("ISY pushed")

    except Exception as e:
        logging.error("Unable to push weather to isy " + str(e))
        print(datetime.datetime.now().time(), "Unable to push weather to isy " + str(e))


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
        # Get ISY security data
        with open(SECRET_FILE, "r") as secret_file:
            user_name = secret_file.readline().strip('\n')
            password = secret_file.readline().strip('\n')

        s = requests.Session()
        update_isy(weather_dict, s, user_name, password)
        s.close()
    except Exception as e:
        logging.error("Unable to update ISY " + str(e))
        print(datetime.datetime.now().time(), "Unable to update ISY " + str(e))


main()
