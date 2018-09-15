#!/usr/bin/python3

import datetime
import json

import syslog

FRONT_YARD = 12147
LIBRARY = 7621
MASTER_BEDROOM_WINDOW = 14129
HUMIDOR = 3329
THEATER_WINDOW = 6227
FRONT_DOOR = 1153

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

	front_yard = ""
	library = ""
	master_bedroom_window = ""
	humidor = ""
	theater_window = ""
	front_door = ""
	all_sensors = ""

	try:
		with open(TEMP_FILE_NAME, "r") as f:
			for line in f:
				parsed_json = json.loads(line)

				if parsed_json['id'] == MASTER_BEDROOM_WINDOW:
					master_bedroom_window = line
				elif parsed_json['id'] == LIBRARY:
					library = line
				elif parsed_json['id'] == HUMIDOR:
					humidor = line
				elif parsed_json['id'] == FRONT_DOOR:
					front_door = line
				elif parsed_json['id'] == THEATER_WINDOW:
					theater_window = line
				elif parsed_json['id'] == FRONT_YARD:
					front_yard = line
	except IOError as e:
		syslog.syslog(syslog.LOG_EMERG, "Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		print(datetime.datetime.now().time(), "Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		pass
	except json.JSONDecodeError as e:
		syslog.syslog(syslog.LOG_EMERG, "Unable to parse weather433.temp " + e.msg)
		print(datetime.datetime.now().time(), "Unable to parse weather433.temp " + e.msg)

	#
	# build the json string
	if master_bedroom_window != "":
		all_sensors = master_bedroom_window

	if library != "":
		all_sensors += library

	if humidor != "":
		all_sensors += humidor

	if front_door != "":
		all_sensors += front_door

	if theater_window != "":
		all_sensors += theater_window

	if front_yard != "":
		all_sensors += front_yard

	return all_sensors


def save_sensor_data(all_sensors):

	try:
		with open(JSON_FILE_NAME, "w+") as f:
			f.write(all_sensors)
	except IOError as e:
		syslog.syslog(syslog.LOG_EMERG, "Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		print(datetime.datetime.now().time(), "Unable to open file " + JSON_FILE_NAME + " " + e.strerror)
		pass


def main():
	all_sensors = get_sensor_data()
	save_sensor_data(all_sensors)

main()
