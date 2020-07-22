#!/usr/bin/python3

import datetime

import httplib2
import syslog
import jsonpickle

from weather import data

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


def get_rest():
    try:
        #
        # call home for data
        h = httplib2.Http(".cache", disable_ssl_certificate_validation=True)
        url = "https://home.evilminions.org/weather/data"
        resp, content = h.request(url, "GET")

        if resp.status != 200:
            syslog.syslog(syslog.LOG_INFO, "Bad response from isy994 " + str(resp))
            print(datetime.datetime.now().time(), " -  Bad response from isy994. " + str(resp))
            return
        json_content = content.decode()
        return jsonpickle.decode(json_content)
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, "Unable to get weather data from home " + e.msg)
        print(datetime.datetime.now().time(), "Unable to get weather data from home " + e.msg)
    return


def push_temp_isy(h, variable_type, variable_id, f_temp, label):
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
    resp, content = h.request(url, "GET")
    if not str(content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
        syslog.syslog(syslog.LOG_INFO, "Failed URL: " + url + " Response: " + str(content))
        print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(content))
    else:
        print(datetime.datetime.now().time(), " - Success URL: ", url)


def update_isy(weather_dict, h):
    push_temp_isy(h, ISY_INTEGER, BACK_YARD_TEMP, weather_dict["back_yard"]["temp"], 'BACK_YARD_TEMP')
    push_temp_isy(h, ISY_INTEGER, MAIN_GARAGE, weather_dict["main_garage"]["temp"], 'MAIN_GARAGE_TEMP')
    push_temp_isy(h, ISY_INTEGER, AVERAGE_HOUSE_TEMP, round(weather_dict["whole_house_fan"]["houseTemp"]), 'AVERAGE_HOUSE_TEMP')
    syslog.syslog(syslog.LOG_CRIT, "ISY Temps pushed")


def main():
    #
    # Get weather data from the rest endpoint
    weather_dict = get_rest()

    #
    # Get ISY security data
    with open(SECRET_FILE, "r") as secret_file:
        user_name = secret_file.readline().strip('\n')
        password = secret_file.readline().strip('\n')

    h = httplib2.Http()
    h.add_credentials(user_name, password)  # Basic authentication
    update_isy(weather_dict, h)


main()
