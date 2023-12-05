import datetime as dt
import requests
import logging
import sys
import utilities.connect as connect
from bs4 import BeautifulSoup

HTTP_URL = 'http://eve4.evilminions.org/'
CONNECT_ITEM_ID = "6a7uy2oo5dtwoomtrojxhaikui"
ZONE_OPEN_COLOR = '#FF0000'
ZONE_OPEN_LABEL = 'OPEN'
ZONE_OPEN = 0
ZONE_CLOSED = 1
FAN_ON = 1
FAN_OFF = 0
COLOR_ATTRIBUTE = 'bgcolor'
# Alarm Status Map
# -1 = Alarm
# 0 = Ready
# >= 10 and < 20 = Not Ready
# >= 20 = Armed

# alarming status
ALARM_STATUS_ALARM_LABEL = 'Alarm'
ALARM_STATUS_ALARM = -1
# not ready status
ALARM_STATUS_NOT_READY_LABEL = 'Not Ready'
ALARM_STATUS_NOT_READY = 10
ALARM_STATUS_NOT_READY_BYPASS_LABEL = 'Not Ready Bypass'
ALARM_STATUS_NOT_READY_BYPASS = 11
ALARM_STATUS_NOT_READY_INSTANT_LABEL = 'Not Ready Instant'
ALARM_STATUS_NOT_READY_INSTANT = 12
ALARM_STATUS_NOT_READY_ALARM_IN_MEMORY_LABEL = 'Not Ready Alarm in Memory'
ALARM_STATUS_NOT_READY_ALARM_IN_MEMORY = 13
ALARM_STATUS_NOT_READY_ENTRY_DELAY_LABEL = 'Not Ready Entry Delay'
ALARM_STATUS_NOT_READY_ENTRY_DELAY = 14
ALARM_STATUS_BUSY_LABEL = 'BUSY'
ALARM_STATUS_BUSY = 15
# ready status
ALARM_STATUS_READY_LABEL = 'Ready'
ALARM_STATUS_READY = 0
# armed status
ALARM_STATUS_ARMED_LABEL = 'Armed'
ALARM_STATUS_ARMED = 20
ALARM_STATUS_ARMED_AWAY_LABEL = 'Armed Away'
ALARM_STATUS_ARMED_AWAY = 21
ALARM_STATUS_ARMED_STAY_LABEL = 'Armed Stay'
ALARM_STATUS_ARMED_STAY = 22
ALARM_STATUS_ARMED_NIGHT_LABEL = 'Armed Night'
ALARM_STATUS_ARMED_NIGHT = 23
ALARM_STATUS_ARMED_BUSY_LABEL = 'BUSY'
ALARM_STATUS_ARMED_BUSY = 24
# alarm status unknown
ALARM_STATUS_UNKNOWN = -999


def get_html():

    try:
        #
        # Get security data
        credentials = connect.get_credentials(CONNECT_ITEM_ID)
        user_name = credentials[0].value
        password = credentials[1].value

        # get EvisaLink4 web
        ret = requests.get(HTTP_URL, auth=(user_name, password), verify=False)
        ret.close()
        if ret.status_code != 200:
            logging.error("Bad response from Evisalink4 " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from Evisalink4. " + str(ret.status_code))
            return ""
        return ret.content.decode()
    except Exception as e:
        logging.error("Unable to get Evisalink4 " + str(e))
        print(dt.datetime.now().time(), "Unable to get Evisalink4 " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            print(dt.datetime.now().time(), "Unable to get Evisalink4 " + str(e))
    return


def parse_html(weather_data, html_document):

    # remove all new lines
    html_document = html_document.replace('\n', '')
    # remove all tabs
    html_document = html_document.replace('\t', '')

    # safe defaults for alarm
    weather_data.alarm.all_zones_closed = 1
    weather_data.whole_house_fan.fan_zones_some = 0
    weather_data.whole_house_fan.fan_zones_all = 0

    soup = BeautifulSoup(html_document, 'html.parser')

    get_zones(weather_data, soup)
    get_status(weather_data, soup)


def get_zones(weather_data, soup):

    all_html_spans = soup.find_all('span')
    for span_html in all_html_spans:
        attributes = span_html.attrs
        title = attributes.get('title')
        label = span_html.text.strip()
        if title and label:
            populate_zone(weather_data, label, title)


def get_status(weather_data, soup):
    all_html_tds = soup.find_all('td')
    previous_label = ""

    for td_html in all_html_tds:
        label = td_html.text.strip()
        if previous_label == "System":
            populate_status(weather_data, label)
        previous_label = label


def populate_status(weather_data, label):

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

        elif label == ALARM_STATUS_ARMED_BUSY_LABEL:
            weather_data.alarm.status_label = ALARM_STATUS_ARMED_NIGHT_LABEL
            weather_data.alarm.status = ALARM_STATUS_ARMED_BUSY

        else:
            weather_data.alarm.status = ALARM_STATUS_UNKNOWN
            logging.error("Unable to get alarm status: " + label)
            print(dt.datetime.now().time(), "Unable to get alarm status: " + label)

    except Exception as e:
        logging.error("Unable to get alarm status:" + label + " " + str(e))
        print(dt.datetime.now().time(), "Unable to get alarm status:" + label + " " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to get alarm status:" + label + " " + str(e))
            print(dt.datetime.now().time(), "Unable to get alarm status:" + label + " " + str(e))


def populate_zone(weather_data, zone, title):

    try:
        zone_status = is_zone_open(title)

        if zone != '1' and zone != '2' and zone != '10' and zone_status == ZONE_OPEN:
            weather_data.whole_house_fan.fan_zones_some = FAN_ON
            weather_data.alarm.all_zones_closed = ZONE_OPEN

        # case on zone
        if zone == '2':
            weather_data.alarm.great_room_motion = zone_status
        elif zone == '3':
            weather_data.alarm.garage_entry_door = zone_status
        elif zone == '4':
            weather_data.alarm.guest_bedrooms_bath = zone_status
        elif zone == '5':
            weather_data.alarm.great_room_windows = zone_status
        elif zone == '6':
            weather_data.alarm.great_room_french_doors = zone_status
        elif zone == '7':
            weather_data.alarm.master_bedroom_window = zone_status
        elif zone == '8':
            weather_data.alarm.master_bathroom_windows = zone_status
        elif zone == '10':
            weather_data.alarm.master_bedroom_motion = zone_status
        elif zone == '11':
            weather_data.alarm.front_entry_door = zone_status
        elif zone == '12':
            weather_data.alarm.den_window = zone_status
        elif zone == '13':
            weather_data.alarm.dining_room_window = zone_status
        elif zone == '14':
            weather_data.alarm.back_patio_door = zone_status

    except Exception as e:
        logging.error("Unable to populate_zone:" + zone + " " + str(e))
        print(dt.datetime.now().time(), "Unable to get status mya:" + zone + " " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to populate_zone:" + zone + " " + str(e))
            print(dt.datetime.now().time(), "Unable to populate_zone:" + zone + " " + str(e))


def is_zone_open(title):

    if title.startswith(ZONE_OPEN_LABEL):
        return ZONE_OPEN
    return ZONE_CLOSED


def determine_fan_status(weather_data):

    if weather_data.alarm.garage_entry_door == ZONE_CLOSED and \
            weather_data.alarm.guest_bedrooms_bath == ZONE_CLOSED and \
            weather_data.alarm.great_room_windows == ZONE_CLOSED and \
            weather_data.alarm.great_room_french_doors == ZONE_CLOSED and \
            weather_data.alarm.master_bedroom_window == ZONE_CLOSED and \
            weather_data.alarm.master_bathroom_windows == ZONE_CLOSED and \
            weather_data.alarm.front_entry_door == ZONE_CLOSED and \
            weather_data.alarm.den_window == ZONE_CLOSED and \
            weather_data.alarm.dining_room_window == ZONE_CLOSED and \
            weather_data.alarm.back_patio_door == ZONE_CLOSED:
        weather_data.whole_house_fan.fan_zones_some = FAN_OFF
        weather_data.alarm.all_zones_closed = ZONE_CLOSED
    else:
        weather_data.alarm.all_zones_closed = ZONE_OPEN

    if weather_data.alarm.guest_bedrooms_bath == ZONE_OPEN \
            and weather_data.alarm.master_bathroom_windows == ZONE_OPEN \
            and weather_data.alarm.master_bedroom_window == ZONE_OPEN:
        weather_data.whole_house_fan.fan_zones_all = FAN_ON
    else:
        weather_data.whole_house_fan.fan_zones_all = FAN_OFF


def get_weather(weather_data):

    try:
        html_response = get_html()
        parse_html(weather_data, html_response)
        determine_fan_status(weather_data)

    except Exception as e:
        logging.error("Unable to get IoX:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get IoX:get_weather " + str(e))
    finally:
        e = sys.exc_info()[0]
        if e:
            logging.error("Unable to get IoX:get_weather " + str(e))
            print(dt.datetime.now().time(), "Unable to get IoX:get_weather " + str(e))
    return
