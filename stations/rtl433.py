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
		sensor = parsed_json.get(THEATER_WINDOW)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.theater_window.humidity = sensor.get(HUMIDITY)
			weather_data.theater_window.temp = temp
			weather_data.theater_window.time = sensor.get(TIME)

		sensor = parsed_json.get(BACK_YARD)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.back_yard.humidity = sensor.get(HUMIDITY)
			weather_data.back_yard.temp = sensor[TEMPERATURE]

		sensor = parsed_json.get(FRONT_DOOR)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.front_door.humidity = sensor.get(HUMIDITY)
			weather_data.front_door.temp = sensor[TEMPERATURE]
			weather_data.front_door.time = sensor.get(TIME)

		sensor = parsed_json.get(LIVING_ROOM_WINDOW)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.living_room_window.humidity = sensor.get(HUMIDITY)
			weather_data.living_room_window.temp = sensor[TEMPERATURE]
			weather_data.living_room_window.time = sensor.get(TIME)

		sensor = parsed_json.get(HUMIDOR)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.humidor.humidity = sensor.get(HUMIDITY)
			weather_data.humidor.temp = sensor[TEMPERATURE]
			weather_data.humidor.time = sensor.get(TIME)

		sensor = parsed_json.get(KITCHEN_THERMOSTAT)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.kitchen_thermostat.temp = sensor[TEMPERATURE]

		sensor = parsed_json.get(LIBRARY)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.library.humidity = sensor.get(HUMIDITY)
			weather_data.library.temp = sensor[TEMPERATURE]
			weather_data.library.time = sensor.get(TIME)

		sensor = parsed_json.get(LIVING_ROOM)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.living_room.humidity = sensor.get(HUMIDITY)
			weather_data.living_room.temp = sensor[TEMPERATURE]

		sensor = parsed_json.get(MASTER_BEDROOM_THERMOSTAT)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.master_bedroom_thermostat.temp = sensor[TEMPERATURE]

		sensor = parsed_json.get(MASTER_BEDROOM_WINDOW)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.master_bedroom_window.humidity = sensor.get(HUMIDITY)
			weather_data.master_bedroom_window.temp = sensor[TEMPERATURE]
			weather_data.master_bedroom_window.time = sensor.get(TIME)

		sensor = parsed_json.get(POOL)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.pool.temp = sensor[TEMPERATURE]

		sensor = parsed_json.get(SPA)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.spa.temp = sensor[TEMPERATURE]

		sensor = parsed_json.get(THEATER)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.theater.humidity = sensor.get(HUMIDITY)
			weather_data.theater.temp = sensor[TEMPERATURE]

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
