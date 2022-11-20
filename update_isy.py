#!/usr/bin/python3

import datetime

import requests
import logging
import jsonpickle

from weather import data
from weather import stations

ISY_INTEGER = 1
ISY_STATE = 2
GARAGE_FREEZER_TEMP = 14
BACK_YARD_TEMP = 13
MAIN_GARAGE = 2
MAIN_GARAGE_TEMP = 18
AVERAGE_HOUSE_TEMP = 25
BIKE_GARAGE = 3
MAIN_GARAGE = 18
MOTORCYCLE_GARAGE = 4
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
    if f_temp == data.DEFAULT_TEMP:
        msg = "Default Temp found for " + label + " Type:" + str(variable_type) + " Id:" + str(variable_id)
        logging.error(msg)
        print(datetime.datetime.now().time(), msg)
        return

    #
    # do a get on isy994 to update the data
    url = "http://isy994.evilminions.org/rest/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(
        round(float(f_temp)))
    ret = s.get(url, auth=(user_name, password), verify=False)
    if not str(ret.content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
        logging.error("Failed URL: " + url + " Response: " + str(ret.content))
        print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(ret.content))
    else:
        print(datetime.datetime.now().time(), " - Success URL: ", url)


def update_isy(weather_dict, s, user_name, password):

    # temps
    push_temp_isy(s, user_name, password, ISY_INTEGER, BACK_YARD_TEMP, weather_dict["back_yard"]["temp"], 'BACK_YARD_TEMP')
    push_temp_isy(s, user_name, password,  ISY_INTEGER, MAIN_GARAGE, weather_dict["main_garage"]["temp"], 'MAIN_GARAGE_TEMP')
    push_temp_isy(s, user_name, password,  ISY_INTEGER, GARAGE_FREEZER_TEMP, weather_dict["main_garage_freezer"]["temp"], 'GARAGE_FREEZER_TEMP')
    push_temp_isy(s, user_name, password,  ISY_INTEGER, AVERAGE_HOUSE_TEMP, round(weather_dict["whole_house_fan"]["houseTemp"]), 'AVERAGE_HOUSE_TEMP')

    # garage doors
    push_temp_isy(s, user_name, password,  ISY_STATE, BIKE_GARAGE, weather_dict["alarm"]["bike_garage"], 'bike_garage')
    push_temp_isy(s, user_name, password,  ISY_STATE, MOTORCYCLE_GARAGE, weather_dict["alarm"]["mc_garage"], 'mc_garage')
    push_temp_isy(s, user_name, password,  ISY_STATE, MAIN_GARAGE, weather_dict["alarm"]["main_garage"], 'main_garage')
    logging.error("ISY pushed")


def main():

    try:
        #
        # Get weather data from the rest endpoint
        # weather_data = stations.get_weather()
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
