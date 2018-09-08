#!/usr/bin/python3

import datetime
import json

import syslog

from weather import data

FRONT_YARD = 12147
LIBRARY = 7621
MASTER_BEDROOM_WINDOW = 14129
HUMIDOR = 3329
THEATER_WINDOW = 6227
FRONT_DOOR = 1153
TEMPERATURE = 'temperature_C'
HUMIDITY = 'humidity'
TIME = 'time'
FILE_NAME = "./data/weather433.json"


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def get_weather(weather_data):
	try:
		with open(FILE_NAME, "r") as f:
			for line in f:
				parse_433_json(weather_data, line)
	except IOError as e:
		syslog.syslog(syslog.LOG_EMERG, "Unable to open file " + FILE_NAME + e.strerror)
		print(datetime.datetime.now().time(), "Unable to open file " + FILE_NAME + e.strerror)
		pass
	finally:
		return weather_data


def parse_433_json(weather_data, line):
	try:
		parsed_json = json.loads(line)

		if parsed_json['id'] == MASTER_BEDROOM_WINDOW:
			weather_data.master_bedroom_window.temp = c_to_f(parsed_json[TEMPERATURE])
			weather_data.master_bedroom_window.humidity = parsed_json[HUMIDITY]
			weather_data.master_bedroom_window.time = parsed_json[TIME]
		elif parsed_json['id'] == LIBRARY:
			weather_data.library.temp = c_to_f(parsed_json[TEMPERATURE])
			weather_data.library.humidity = parsed_json[HUMIDITY]
			weather_data.library.time = parsed_json[TIME]
		elif parsed_json['id'] == HUMIDOR:
			weather_data.humidor.temp = c_to_f(parsed_json[TEMPERATURE])
			weather_data.humidor.humidity = parsed_json[HUMIDITY]
			weather_data.humidor.time = parsed_json[TIME]
		elif parsed_json['id'] == FRONT_DOOR:
			weather_data.front_door.temp = c_to_f(parsed_json[TEMPERATURE])
			weather_data.front_door.humidity = parsed_json[HUMIDITY]
			weather_data.front_door.time = parsed_json[TIME]
		elif parsed_json['id'] == THEATER_WINDOW:
			weather_data.theater_window.temp = c_to_f(parsed_json[TEMPERATURE])
			weather_data.theater_window.humidity = parsed_json[HUMIDITY]
			weather_data.theater_window.time = parsed_json[TIME]
		elif parsed_json['id'] == FRONT_YARD:
			weather_data.front_yard.temp = c_to_f(parsed_json[TEMPERATURE])
			weather_data.front_yard.humidity = parsed_json[HUMIDITY]
			weather_data.front_yard.time = parsed_json[TIME]
	except json.JSONDecodeError as e:
		syslog.syslog(syslog.LOG_EMERG, "Unable to parse weather433.json " + e.msg)
		print(datetime.datetime.now().time(), "Unable to parse weather433.json " + e.msg)
	finally:
		return weather_data


def main():
	cur_weather = data.WeatherData()
	get_weather(cur_weather)


main()
