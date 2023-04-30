#!/usr/bin/python3

import datetime
import json
import sys
import logging
import requests
from weather import data

BACK_YARD = 'back_yard'
EQ_RACK = 'rack'
EQ_PANEL = 'panel'
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
TEMPERATURE_C = 'temp_c'
HUMIDITY = 'humidity'
TIME = 'time'
S_OK = 200


def rtl_433_json(host):
	#
	# Pull the json from 433 enabled pi
	url = "http://" + host + ":8080/weather"

	try:
		#
		# Pull the data
		ret = requests.get(url, verify=False)
		ret.close()
		if ret.status_code != 200:
			logging.error("Bad response from rtl_433_json " + str(ret.status_code))
			print(datetime.datetime.now().time(), " -  Bad response from rtl_433_json. " + str(ret.status_code))
		return json.loads(ret.content.decode())
	except Exception as e:
		logging.error( "Unable to parse rtl_433_json " + str(e))
		print(datetime.datetime.now().time(), "Unable to parse rtl_433_json " + str(e))
	return


def get_weather(weather_data, host):

	try:
		parsed_json = rtl_433_json(host)

		sensor = parsed_json.get(EQ_RACK)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.rack.humidity = sensor.get(HUMIDITY)
			weather_data.rack.temp = temp
			weather_data.rack.temp_c = sensor.get(TEMPERATURE_C)
			weather_data.rack.time = sensor.get(TIME)

		sensor = parsed_json.get(EQ_PANEL)
		temp = sensor.get(TEMPERATURE)
		if temp != data.DEFAULT_TEMP:
			weather_data.panel.humidity = sensor.get(HUMIDITY)
			weather_data.panel.temp = temp
			weather_data.panel.temp_c = sensor.get(TEMPERATURE_C)
			weather_data.panel.time = sensor.get(TIME)

	except json.JSONDecodeError as e:
		logging.error("Unable to parse rtl433 " + str(e))
		print(datetime.datetime.now().time(), "Unable to parse rtl433 " + str(e))
	except TypeError as e:
		logging.error("Unable to parse rtl433: TypeError " + str(e))
		print(datetime.datetime.now().time(), "Unable to parse rtl433: TypeError " + str(e))
	except Exception as e:
		logging.error("Unable to get rtl433:get_weather " + str(e))
		print(datetime.datetime.now().time(), "Unable to get rtl433:get_weather " + str(e))
	except:
		e = sys.exc_info()[0]
		logging.error("Unable to get rtl433:get_weather " + str(e))
		print(datetime.datetime.now().time(), "Unable to get rtl433:get_weather " + str(e))
	return

