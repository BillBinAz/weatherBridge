#!/usr/bin/python3

import datetime

import requests
import urllib3
import logging


def get_rest():
    try:
        #
        # call home for data
        url = "https://home.evilminions.org/weather/data"
        ret = requests.get(url, verify=False)

        if ret.status_code != 200:
            logging.error("Bad response from IoX " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  Bad response from IoX. " + str(ret.status_code))
            return
        return ret.content.decode()

    except Exception as e:
        logging.error("Unable to get weather data from home " + str(e))
        print(datetime.datetime.now().time(), "Unable to get weather data from home " + str(e))
    return


def main():

    try:
        #
        urllib3.disable_warnings()
        print(get_rest())

    except Exception as e:
        logging.error("Unable to get fan speed " + str(e))
        print(datetime.datetime.now().time(), "Unable to get fan speed " + str(e))


main()
