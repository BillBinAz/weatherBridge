#!/usr/bin/python3

import datetime
import json

import requests
import syslog

from weather import data

BACK_YARD = 'back_yard'
FRONT_DOOR = 'front_door'
HUMIDOR = 'humidor'
KITCHEN_THERMOSTAT = 'kitchen_thermostat'
LIBRARY = 'library'
LIVING_ROOM = 'living_room'
LIVING_ROOM_WINDOW = 'living_room_window'
MASTER_BEDROOM_THERMOSTAT = 'master_bedroom_thermostat'
MASTER_BEDROOM_WINDOW = 'master_bedroom_window'
MAIN_GARAGE = 'main_garage'
POOL = 'pool'
SPA = 'spa'
THEATER = 'theater'
THEATER_WINDOW = 'theater_window'
TEMPERATURE = 'temp'
HUMIDITY = 'humidity'
TIME = 'time'
S_OK = 200


def rtl_433_json(host):
	#
	# Pull the json from 433 enabled pi
	response = requests.get("http://" + host + ":8080/weather")
	if not response.ok:
		syslog.syslog(syslog.LOG_INFO, "Bad response from " + str(host) + " " + str(response))
		print(datetime.datetime.now().time(), " -  Bad response from " + str(host) + " " + str(response))
	return response.json()


def get_weather(weather_data, host):

	try:
		parsed_json = rtl_433_json(host)
		sensor = parsed_json.get(MAIN_GARAGE)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.main_garage.humidity = sensor.get(HUMIDITY)
			weather_data.main_garage.temp = temp
			weather_data.main_garage.time = sensor.get(TIME)

		sensor = parsed_json.get(HUMIDOR)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.humidor.humidity = sensor.get(HUMIDITY)
			weather_data.humidor.temp = sensor[TEMPERATURE]
			weather_data.humidor.time = sensor.get(TIME)

	except json.JSONDecodeError as e:
		syslog.syslog(syslog.LOG_INFO, "Unable to parse kiosk " + e.msg)
		print(datetime.datetime.now().time(), "Unable to parse kiosk " + e.msg)
	except TypeError as e:
		syslog.syslog(syslog.LOG_INFO, "Unable to parse kiosk: TypeError " + e.msg)
		print(datetime.datetime.now().time(), "Unable to parse kiosk: TypeError " + e.msg)
	finally:
		return weather_data


def main():

	cur_weather = data.WeatherData()
	# get_weather(cur_weather, "kiosk.evilminions.org")
	# get_weather(cur_weather, "cairo.evilminions.org")
	# print(cur_weather.to_json())


main()
