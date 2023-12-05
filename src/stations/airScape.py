#!/usr/bin/python3

import datetime as dt
import xml.etree.ElementTree
import requests
import logging
import sys
import utilities.conversions as conversions


def get_node_xml():

    try:
        url = "http://fan.evilminions.org/status.xml.cgi"
        ret = requests.post(url, verify=False)
        ret.close()
        if ret.status_code != 200:
            logging.error("Bad response from AirScape " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from AirScape. " + str(ret.status_code))
            return
        return xml.etree.ElementTree.fromstring(clean_up_xml(ret.content))
    except Exception as e:
        logging.error("Unable to parse AirScape " + str(e))
        print(dt.datetime.now().time(), "Unable to parse AirScape " + str(e))
    return


def clean_up_xml(content):
    try:
        str_content = content.decode("utf=8", "ignore")
        start = str_content.find("<server_response>")
        end = str_content.find("</server_response>") + len("</server_response>")
        return str_content.replace(str_content[start:end], "").replace("\n", "")
    except Exception as e:
        logging.error("Unable to get AirScape " + str(e))
        print(dt.datetime.now().time(), "Unable to get AirScape " + str(e))
    return


def get_weather(weather_data):

    try:
        xml_response = get_node_xml()
        weather_data.whole_house_fan.atticTemp = xml_response.find('attic_temp').text
        weather_data.whole_house_fan.speed = xml_response.find('fanspd').text
        weather_data.whole_house_fan.cubitFeetPerMinute = xml_response.find('cfm').text
        weather_data.whole_house_fan.power = xml_response.find('power').text
        hours = int(xml_response.find('timeremaining').text) / 60
        weather_data.whole_house_fan.timeRemaining = conversions.format_f(hours, 'timeremaining')
    except Exception as e:
        logging.error("Unable to get AirScape:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get AirScape:get_weather " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get AirScape:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get AirScape:get_weather " + str(e))
    return
