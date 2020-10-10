#!/usr/bin/python3

import datetime

import requests
import syslog
import jsonpickle
import urllib3

ISY_INTEGER = 1
ISY_STATE = 2
FRONT_DOOR_TEMP = 12
BACK_YARD_TEMP = 13
THEATER_WINDOW_TEMP = 14
MASTER_BEDROOM_TEMP = 17
LIVING_ROOM_WINDOW = 22
MAIN_GARAGE = 18
AVERAGE_HOUSE_TEMP = 25


def get_rest():
    try:
        #
        # call home for data
        url = "https://home.evilminions.org/weather/data"
        ret = requests.get(url, verify=False)

        if ret.status_code != 200:
            syslog.syslog(syslog.LOG_CRIT, "Bad response from isy994 " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  Bad response from isy994. " + str(ret.status_code))
            return
        json_content = ret.content.decode()
        return jsonpickle.decode(json_content)
    except Exception as e:
        syslog.syslog(syslog.LOG_CRIT, "Unable to get weather data from home " + str(e))
        print(datetime.datetime.now().time(), "Unable to get weather data from home " + str(e))
    return


def main():

    try:
        #
        # Get weather data from the rest endpoint
        # weather_data = stations.get_weather()
        urllib3.disable_warnings()
        weather_dict = get_rest()

        print("{ \"fanSpeed\" : %s, \"indoorTemp\" : %s, \"outdoorTemp\" : %s }" %
              (weather_dict["whole_house_fan"]["speed"],
              weather_dict["back_yard"]["temp"],
              weather_dict["whole_house_fan"]["houseTemp"]))


    except Exception as e:
        syslog.syslog(syslog.LOG_CRIT, "Unable to get fan speed " + str(e))
        print(datetime.datetime.now().time(), "Unable to get fan speed " + str(e))


main()
