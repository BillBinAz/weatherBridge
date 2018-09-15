#!/usr/bin/python3

import datetime
import json

import httplib2
import syslog

from weather import data

BACK_YARD = 'back_yard'
FRONT_DOOR = 'front_door'
FRONT_YARD = 'front_yard'
HUMIDOR = 'humidor'
KITCHEN_THERMOSTAT = 'kitchen_thermostat'
LIBRARY = 'library'
LIVING_ROOM = 'living_room'
MASTER_BEDROOM_THERMOSTAT = 'master_bedroom_thermostat'
MASTER_BEDROOM_WINDOW = 'master_bedroom_window'
POOL = 'pool'
SPA = 'spa'
THEATER = 'theater'
THEATER_WINDOW = 'theater_window'
TEMPERATURE = 'temp'
HUMIDITY = 'humidity'
S_OK = 200


def rtl_433_json():

	#
	# Pull the XML from meteobridge
	h = httplib2.Http()
	resp, content = h. \
		request("http://kiosk.evilminions.org:8080/weather", "GET")
	if resp.status != S_OK:
		syslog.syslog(syslog.LOG_EMERG, "Bad response from kiosk " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from kiosk. " + str(resp))

	return content


def get_weather(weather_data):
	try:
		parsed_json = json.loads(rtl_433_json())

		sensor = parsed_json[BACK_YARD]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.back_yard.humidity = sensor[HUMIDITY]
			weather_data.back_yard.temp = sensor[TEMPERATURE]

		sensor = parsed_json[FRONT_DOOR]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.front_door.humidity = sensor[HUMIDITY]
			weather_data.front_door.temp = sensor[TEMPERATURE]

		sensor = parsed_json[FRONT_YARD]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.front_yard.humidity = sensor[HUMIDITY]
			weather_data.front_yard.temp = sensor[TEMPERATURE]

		sensor = parsed_json[HUMIDOR]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.humidor.humidity = sensor[HUMIDITY]
			weather_data.humidor.temp = sensor[TEMPERATURE]

		sensor = parsed_json[KITCHEN_THERMOSTAT]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.kitchen_thermostat.temp = sensor[TEMPERATURE]

		sensor = parsed_json[LIBRARY]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.library.humidity = sensor[HUMIDITY]
			weather_data.library.temp = sensor[TEMPERATURE]

		sensor = parsed_json[LIVING_ROOM]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.living_room.humidity = sensor[HUMIDITY]
			weather_data.living_room.temp = sensor[TEMPERATURE]

		sensor = parsed_json[MASTER_BEDROOM_THERMOSTAT]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.master_bedroom_thermostat.temp = sensor[TEMPERATURE]

		sensor = parsed_json[MASTER_BEDROOM_WINDOW]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.master_bedroom_window.humidity = sensor[HUMIDITY]
			weather_data.master_bedroom_window.temp = sensor[TEMPERATURE]

		sensor = parsed_json[POOL]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.pool.temp = sensor[TEMPERATURE]

		sensor = parsed_json[SPA]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.spa.temp = sensor[TEMPERATURE]

		sensor = parsed_json[THEATER]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.theater.humidity = sensor[HUMIDITY]
			weather_data.theater.temp = sensor[TEMPERATURE]

		sensor = parsed_json[THEATER_WINDOW]
		temp = sensor['temp']
		if temp != data.DEFAULT_TEMP:
			weather_data.theater_window.humidity = sensor[HUMIDITY]
			weather_data.theater_window.temp = sensor[TEMPERATURE]

	except json.JSONDecodeError as e:
		syslog.syslog(syslog.LOG_EMERG, "Unable to parse kiosk " + e.msg)
		print(datetime.datetime.now().time(), "Unable to parse kiosk " + e.msg)
	except:
		print("unknown error")
	finally:
		return weather_data


def main():
	cur_weather = data.WeatherData()
	get_weather(cur_weather)
	print(cur_weather.to_json())


main()
