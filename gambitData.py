#!/usr/bin/python3

import datetime

import requests
import syslog
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
        return ret.content.decode()

    except Exception as e:
        syslog.syslog(syslog.LOG_CRIT, "Unable to get weather data from home " + str(e))
        print(datetime.datetime.now().time(), "Unable to get weather data from home " + str(e))
    return


def main():

    try:
        #
        urllib3.disable_warnings()
        print(get_rest())

    except Exception as e:
        syslog.syslog(syslog.LOG_CRIT, "Unable to get fan speed " + str(e))
        print(datetime.datetime.now().time(), "Unable to get fan speed " + str(e))


main()
