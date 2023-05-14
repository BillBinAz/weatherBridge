import datetime
import requests
import logging
import sys
from bs4 import BeautifulSoup

HTTP_URL = 'http://192.168.0.7'
SECRET_FILE = "./secret/evisalink4"
ZONE_OPEN_COLOR = '#FF0000'
ZONE_OPEN = 0
ZONE_CLOSED = 1
FAN_ON = 1
FAN_OFF = 0
COLOR_ATTRIBUTE = 'bgcolor'
ALARM_STATUS_UNKNOWN = -999
ALARM_STATUS_NOT_READY_LABEL = 'Not Ready'
ALARM_STATUS_NOT_READY = 0
ALARM_STATUS_READY_LABEL = 'Ready'
ALARM_STATUS_READY = 1
ALARM_STATUS_ARMED_LABEL = 'Armed'
ALARM_STATUS_ARMED = 2
ALARM_STATUS_ARMED_AWAY_LABEL = 'Armed Away'
ALARM_STATUS_ARMED_AWAY = 3
ALARM_STATUS_ARMED_STAY_LABEL = 'Armed Stay'
ALARM_STATUS_ARMED_STAY = 4
ALARM_STATUS_ARMED_NIGHT_LABEL = 'Armed Night'
ALARM_STATUS_ARMED_NIGHT = 5
ALARM_STATUS_ALARM_LABEL = 'Alarm'
ALARM_STATUS_ALARM = -1
ALARM_STATUS_NOT_READY_BYPASS_LABEL = 'Not Ready Bypass'
ALARM_STATUS_NOT_READY_BYPASS = 6
ALARM_STATUS_NOT_READY_INSTANT_LABEL = 'Not Ready Instant'
ALARM_STATUS_NOT_READY_INSTANT = 7
ALARM_STATUS_NOT_READY_ALARM_IN_MEMORY_LABEL = 'Not Ready Alarm in Memory'
ALARM_STATUS_NOT_READY_ALARM_IN_MEMORY = 8
ALARM_STATUS_NOT_READY_ENTRY_DELAY_LABEL = 'Not Ready Entry Delay'
ALARM_STATUS_NOT_READY_ENTRY_DELAY = 9


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
    previous_label = ""

    for td_html in all_html_tds:
        # find the ones with colors
        attributes = td_html.attrs
        color = attributes.get(COLOR_ATTRIBUTE)
        label = td_html.text.strip()
        if color and label:
            populate_zone(weather_data, label, color)
        if previous_label == "System":
            populate_status(weather_data, label, color)
        previous_label = label


def populate_status(weather_data, label, color):
    try:
        weather_data.alarm.status_label = label

        if label == ALARM_STATUS_NOT_READY_LABEL:
            weather_data.alarm.status = ALARM_STATUS_NOT_READY

        elif label == ALARM_STATUS_READY_LABEL:
            weather_data.alarm.status = ALARM_STATUS_READY

        elif label == ALARM_STATUS_ARMED_LABEL:
            weather_data.alarm.status = ALARM_STATUS_ARMED

        elif label == ALARM_STATUS_ARMED_AWAY_LABEL:
            weather_data.alarm.status = ALARM_STATUS_ARMED_AWAY

        elif label == ALARM_STATUS_ARMED_STAY_LABEL:
            weather_data.alarm.status = ALARM_STATUS_ARMED_STAY

        elif label == ALARM_STATUS_ARMED_NIGHT_LABEL:
            weather_data.alarm.status = ALARM_STATUS_ARMED_NIGHT

        elif label == ALARM_STATUS_ALARM_LABEL:
            weather_data.alarm.status = ALARM_STATUS_ALARM

        elif label == ALARM_STATUS_NOT_READY_BYPASS_LABEL:
            weather_data.alarm.status = ALARM_STATUS_NOT_READY_BYPASS

        elif label == ALARM_STATUS_NOT_READY_INSTANT_LABEL:
            weather_data.alarm.status = ALARM_STATUS_NOT_READY_INSTANT

        elif label == ALARM_STATUS_NOT_READY_ALARM_IN_MEMORY_LABEL:
            weather_data.alarm.status = ALARM_STATUS_NOT_READY_ALARM_IN_MEMORY

        elif label == ALARM_STATUS_NOT_READY_ENTRY_DELAY_LABEL:
            weather_data.alarm.status = ALARM_STATUS_NOT_READY_ENTRY_DELAY

        else:
            weather_data.alarm.status = ALARM_STATUS_UNKNOWN
            logging.error("Unable to get alarm status: " + label)
            print(datetime.datetime.now().time(), "Unable to get alarm status: " + label)

    except Exception as e:
        logging.error("Unable to get alarm status:" + label + " " + str(e))
        print(datetime.datetime.now().time(), "Unable to get alarm status:" + label + " " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to get alarm status:" + label + " " + str(e))
            print(datetime.datetime.now().time(), "Unable to get alarm status:" + label + " " + str(e))


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

    if color == ZONE_OPEN_COLOR:
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
