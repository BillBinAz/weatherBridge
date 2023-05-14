import datetime
import requests
import logging
import xml.etree.ElementTree
import sys

HTTP_URL = 'http://192.168.0.7'
SECRET_FILE = "./secret/evisalink4"
COLOR_ZONE_OPEN = 'FF0000'
ZONE_OPEN = 0
ZONE_CLOSED = 1
FAN_ON = 1
FAN_OFF = 0


def get_html():

    try:
        # Get Evisalink4 security data
        with open(SECRET_FILE, "r") as secret_file:
            user_name = secret_file.readline().strip('\n')
            password = secret_file.readline().strip('\n')

        # get EvisaLink4 web
        ret = requests.get(HTTP_URL, auth=(user_name, password), verify=False)
        ret.close()
        if ret.status_code != 200:
            logging.error("Bad response from Evisalink4 " + str(ret.status_code))
            print(datetime.datetime.now().time(), " -  Bad response from Evisalink4. " + str(ret.status_code))
            return ""
        return ret.content.decode()
    except Exception as e:
        logging.error("Unable to get Evisalink4 " + str(e))
        print(datetime.datetime.now().time(), "Unable to get Evisalink4 " + str(e))
    return


def parse_zone_info(weather_data, http_response):

    try:
        zone_info = extract_zone(http_response)
        zone_id = 0
        start = 0

        for i in range(16):
            zone_id += 1
            start = zone_info.find("<TD BGCOLOR=", start)
            color = zone_info[start+13:start+19]
            populate_zone(weather_data, zone_id, color)

            start += len("<TD BGCOLOR=")

    except Exception as e:
        logging.error("Unable to get Evisalink4 " + str(e))
        print(datetime.datetime.now().time(), "Unable to get Evisalink4 " + str(e))
    return


def populate_zone(weather_data, zone, color):

    zone_status = is_zone_open(color)

    if zone != 2 and zone_status == ZONE_OPEN:
        weather_data.whole_house_fan.fan_zones_some = FAN_ON

    # case on zone
    if zone == 1:
        weather_data.alarm.front_garage_door = zone_status
    elif zone == 2:
        weather_data.alarm.sliding_glass_door = zone_status
    elif zone == 3:
        weather_data.alarm.living_great = zone_status
    elif zone == 4:
        weather_data.alarm.master = zone_status
    elif zone == 5:
        weather_data.alarm.offices = zone_status
    elif zone == 6:
        weather_data.alarm.west_wing = zone_status
    elif zone == 10:
        weather_data.alarm.bike_garage = zone_status


def is_zone_open(color):

    if color == COLOR_ZONE_OPEN:
        return ZONE_OPEN
    return ZONE_CLOSED


def extract_zone(http_response):

    # remove all new lines
    http_response = http_response.replace('\n', '')
    # remove all tabs
    http_response = http_response.replace('\t', '')
    # find location of string
    start = http_response.find("<TABLE BORDER=2 CLASS=keypad>")
    # from start find </table>
    end = http_response.find("</TABLE>", start) + len("</TABLE>")
    # get substring
    zone_info = http_response[start:end]

    return zone_info


def determine_fan_status(weather_data):

    if weather_data.alarm.west_wing == ZONE_OPEN \
            and weather_data.alarm.master == ZONE_OPEN and weather_data.alarm.living_great == ZONE_OPEN:
        weather_data.whole_house_fan.fan_zones_all = FAN_ON
    else:
        weather_data.whole_house_fan.fan_zones_all = FAN_OFF


def get_weather(weather_data):

    try:
        html_response = get_html()
        parse_zone_info(weather_data, html_response)
        determine_fan_status(weather_data)

    except Exception as e:
        logging.error("Unable to get isy994:get_weather " + str(e))
        print(datetime.datetime.now().time(), "Unable to get isy994:get_weather " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get isy994:get_weather " + str(e))
        print(datetime.datetime.now().time(), "Unable to get isy994:get_weather " + str(e))
    return
