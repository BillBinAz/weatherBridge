import datetime
import requests
import logging
import sys
from bs4 import BeautifulSoup

HTTP_URL = 'http://192.168.0.7'
SECRET_FILE = "./secret/evisalink4"
COLOR_ZONE_OPEN = '#FF0000'
ZONE_OPEN = 0
ZONE_CLOSED = 1
FAN_ON = 1
FAN_OFF = 0
COLOR_ATTRIBUTE = 'bgcolor'


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
    finally:
        e = sys.exc_info()[0]
        if e:
            print(datetime.datetime.now().time(), "Unable to get Evisalink4 " + str(e))
    return


def parse_html(weather_data, html_document):

    # remove all new lines
    html_document = html_document.replace('\n', '')
    # remove all tabs
    html_document = html_document.replace('\t', '')

    soup = BeautifulSoup(html_document, 'html.parser')
    all_html_tds = soup.find_all('td')

    for td_html in all_html_tds:
        # find the ones with colors
        attributes = td_html.attrs
        color = attributes.get(COLOR_ATTRIBUTE)
        label = td_html.text
        if color and label:
            populate_zone(weather_data, label, color)


def populate_zone(weather_data, zone, color):

    try:
        zone_status = is_zone_open(color)

        if zone != 2 and zone_status == ZONE_OPEN:
            weather_data.whole_house_fan.fan_zones_some = FAN_ON
            weather_data.alarm.all_zones_closed = ZONE_OPEN
        # case on zone
        if zone == '1':
            weather_data.alarm.front_garage_door = zone_status
        elif zone == '2':
            weather_data.alarm.sliding_glass_door = zone_status
        elif zone == '3':
            weather_data.alarm.living_great = zone_status
        elif zone == '4':
            weather_data.alarm.master = zone_status
        elif zone == '5':
            weather_data.alarm.offices = zone_status
        elif zone == '6':
            weather_data.alarm.west_wing = zone_status
        elif zone == '10':
            weather_data.alarm.bike_garage = zone_status
    except Exception as e:
        logging.error("Unable to populate_zone:" + zone + " " + str(e))
        print(datetime.datetime.now().time(), "Unable to get status mya:" + zone + " " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to populate_zone:" + zone + " " + str(e))
            print(datetime.datetime.now().time(), "Unable to populate_zone:" + zone + " " + str(e))


def is_zone_open(color):

    if color == COLOR_ZONE_OPEN:
        return ZONE_OPEN
    return ZONE_CLOSED


def determine_fan_status(weather_data):

    if weather_data.alarm.front_garage_door == ZONE_CLOSED and \
            weather_data.alarm.living_great == ZONE_CLOSED and \
            weather_data.alarm.master == ZONE_CLOSED and \
            weather_data.alarm.offices == ZONE_CLOSED and \
            weather_data.alarm.west_wing == ZONE_CLOSED:
        weather_data.whole_house_fan.fan_zones_some = FAN_OFF
        weather_data.alarm.all_zones_closed = ZONE_CLOSED
    else:
        weather_data.alarm.all_zones_closed = ZONE_OPEN

    if weather_data.alarm.west_wing == ZONE_OPEN \
            and weather_data.alarm.master == ZONE_OPEN \
            and weather_data.alarm.living_great == ZONE_OPEN:
        weather_data.whole_house_fan.fan_zones_all = FAN_ON
    else:
        weather_data.whole_house_fan.fan_zones_all = FAN_OFF


def get_weather(weather_data):

    try:
        html_response = get_html()
        parse_html(weather_data, html_response)
        determine_fan_status(weather_data)

    except Exception as e:
        logging.error("Unable to get isy994:get_weather " + str(e))
        print(datetime.datetime.now().time(), "Unable to get isy994:get_weather " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to get isy994:get_weather " + str(e))
            print(datetime.datetime.now().time(), "Unable to get isy994:get_weather " + str(e))
    return
