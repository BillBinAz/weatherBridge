#!/usr/bin/python3

import datetime as dt
import json
import logging

LIBRARY = 7621
EQ_RACK = 14129
HUMIDOR = 3329
EQ_PANEL = 6227
GARAGE = 9957

TEMPERATURE = 'temperature_C'
HUMIDITY = 'humidity'
TIME = 'time'

TEMP_FILE_NAME = "/tmp/weather433.temp"
JSON_FILE_NAME = "/tmp/weather433.json"


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def get_sensor_data():

	rack = ""
	humidor = ""
	panel = ""
	all_sensors = ""
	garage = ""

	try:
		with open(TEMP_FILE_NAME, "r") as f:
			for line in f:
				parsed_json = json.loads(line)

				if parsed_json['id'] == EQ_RACK:
					rack = line
				elif parsed_json['id'] == LIBRARY:
					library = line
				elif parsed_json['id'] == HUMIDOR:
					humidor = line
				elif parsed_json['id'] == EQ_PANEL:
					panel = line
				elif parsed_json['id'] == GARAGE:
					garage = line
	except IOError as e:
		logging.info("Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		print(dt.datetime.now().time(), "Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		pass
	except json.JSONDecodeError as e:
		logging.error("Unable to parse weather433.temp " + e.msg)
		print(dt.datetime.now().time(), "Unable to parse weather433.temp " + e.msg)

	#
	# build the json string
	if rack != "":
		all_sensors = rack

	if humidor != "":
		all_sensors += humidor

	if panel != "":
		all_sensors += panel

	if garage != "":
		all_sensors += garage

	return all_sensors


def save_sensor_data(all_sensors):

	try:
		with open(JSON_FILE_NAME, "w+") as f:
			f.write(all_sensors)
	except IOError as e:
		logging.error("Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		print(dt.datetime.now().time(), "Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		pass


def main():
	all_sensors = get_sensor_data()
	save_sensor_data(all_sensors)

main()
