#!/usr/bin/python3

import datetime

import httplib2
import syslog

from weather import data
from weather import stations

ISY_INTEGER = 1
ISY_STATE = 2
FRONT_DOOR_TEMP = 12
BACK_YARD_TEMP = 13
THEATER_WINDOW_TEMP = 14
MASTER_BEDROOM_TEMP = 17
LIVING_ROOM_WINDOW = 22
MAIN_GARAGE = 18
AVERAGE_HOUSE_TEMP = 25
SECRET_FILE = "./secret/isy994"


def push_temp_isy(variable_type, variable_id, f_temp, label):
    #
    # Never push defaults to ISY
    if f_temp == data.DEFAULT_TEMP:
        msg = "Default Temp found for " + label + " Type:" + str(variable_type) + " Id:" + str(variable_id)
        syslog.syslog(syslog.LOG_CRIT, msg)
        print(datetime.datetime.now().time(), msg)
        return

    #
    # Get ISY security data
    with open(SECRET_FILE, "r") as secret_file:
        user_name = secret_file.readline().strip('\n')
        password = secret_file.readline().strip('\n')

    #
    # do a get on isy994 to update the data
    url = "http://isy994.evilminions.org/rest/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(
        round(float(f_temp)))
    h = httplib2.Http()
    h.add_credentials(user_name, password)  # Basic authentication
    resp, content = h.request(url, method="GET", headers={'Connection': 'close'})
    if not str(content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
        syslog.syslog(syslog.LOG_INFO, "Failed URL: " + url + " Response: " + str(content))
        print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(content))
    else:
        print(datetime.datetime.now().time(), " - Success URL: ", url)


def update_isy(weather_data):
    push_temp_isy(ISY_INTEGER, BACK_YARD_TEMP, weather_data.back_yard.temp, 'BACK_YARD_TEMP')
    push_temp_isy(ISY_INTEGER, MAIN_GARAGE, weather_data.main_garage.temp, 'MAIN_GARAGE_TEMP')
    push_temp_isy(ISY_INTEGER, AVERAGE_HOUSE_TEMP, round(weather_data.whole_house_fan.houseTemp), 'AVERAGE_HOUSE_TEMP')
    syslog.syslog(syslog.LOG_CRIT, "ISY Temps pushed")


def main():
    weather_data = stations.get_weather()
    # print(weather_data.to_json())
    update_isy(weather_data)


main()
