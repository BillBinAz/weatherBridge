#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import httplib2
import syslog

from weather import data

S_OK = 200
TEMPERATURE = 'temp'
HUMIDITY = 'hum'
DEP_POINT = 'dew'

MASTER_BEDROOM_WINDOW = "th5"
THEATER_WINDOW = "th6"
FRONT_WINDOW = "th7"
LIBRARY = "th8"
HUMIDOR = "th9"
SECRET_FILE = "./secret/meteobridge"


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def get_meteobridge_xml():
	#
	# Get the username/password from the secret file
	with open(SECRET_FILE, "r") as secret_file:
		user_name = secret_file.readline().strip('\n')
		password = secret_file.readline().strip('\n')

	#
	# Pull the XML from meteobridge
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h. \
		request("http://meteobridge/cgi-bin/livedataxml.cgi", "GET")
	if resp.status != S_OK:
		syslog.syslog(syslog.LOG_EMERG, "Bad response from meteobridge " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from meteobridge. " + str(resp))
	xml_response = xml.etree.ElementTree.fromstring(content)
	return xml_response


def get_weather(weather_data):
	#
	# Process the XML Variables
	meteobridge_xml = get_meteobridge_xml()
	for sensor in meteobridge_xml.findall('TH'):
		if sensor.get('id') == MASTER_BEDROOM_WINDOW:
			weather_data.master_bedroom_window.temp = c_to_f(sensor.get(TEMPERATURE))
			weather_data.master_bedroom_window.humidity = sensor.get(HUMIDITY)
			weather_data.master_bedroom_window.dew_point = c_to_f(sensor.get(DEP_POINT))
		elif sensor.get('id') == LIBRARY:
			weather_data.library.temp = c_to_f(sensor.get(TEMPERATURE))
			weather_data.library.humidity = sensor.get(HUMIDITY)
			weather_data.library.dew_point = c_to_f(sensor.get(DEP_POINT))
		elif sensor.get('id') == HUMIDOR:
			weather_data.humidor.temp = c_to_f(sensor.get(TEMPERATURE))
			weather_data.humidor.humidity = sensor.get(HUMIDITY)
			weather_data.humidor.dew_point = c_to_f(sensor.get(DEP_POINT))
		elif sensor.get('id') == FRONT_WINDOW:
			weather_data.front_door.temp = c_to_f(sensor.get(TEMPERATURE))
			weather_data.front_door.humidity = sensor.get(HUMIDITY)
			weather_data.front_door.dew_point = c_to_f(sensor.get(DEP_POINT))
		elif sensor.get('id') == THEATER_WINDOW:
			weather_data.theater_window.temp = c_to_f(sensor.get(TEMPERATURE))
			weather_data.theater_window.humidity = sensor.get(HUMIDITY)
			weather_data.theater_window.dew_point = c_to_f(sensor.get(DEP_POINT))

	return weather_data


def main():
	cur_weather = data.WeatherData()
	get_weather(cur_weather)


main()
