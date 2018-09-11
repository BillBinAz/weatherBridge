#!/usr/bin/python3

import datetime

import httplib2
import syslog

from weather import data
from weather import stations

ISY_STATE = 2
FRONT_DOOR_TEMP = 1
BACK_YARD_TEMP = 2
THEATER_WINDOW_TEMP = 5
MASTER_BEDROOM_TEMP = 12
TEMPERATURE_BUFFER = 3
SECRET_FILE = "./secret/isy994"


def push_temp_isy(variable_type, variable_id, f_temp, label):

	#
	# Never push defaults to ISY
	if f_temp == data.DEFAULT_TEMP:
		syslog.syslog(syslog.LOG_CRIT, "Default Temp found for " + label + " Type:" + str(variable_type) + " Id:" + str(variable_id))
		return

	#
	# Get ISY security data
	with open(SECRET_FILE, "r") as secret_file:
		user_name = secret_file.readline().strip('\n')
		password = secret_file.readline().strip('\n')

	f_temp = f_temp + TEMPERATURE_BUFFER

	#
	# do a get on isy994 to update the data
	url = "http://isy994.evilminions.org/rest/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(
		round(f_temp))
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h.request(url, "GET")
	if not str(content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
		syslog.syslog(syslog.LOG_EMERG, "Failed URL: " + url + " Response: " + str(content))
		print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(content))
	else:
		print(datetime.datetime.now().time(), " - Success URL: ", url)


def update_isy(weather_data):
	push_temp_isy(ISY_STATE, BACK_YARD_TEMP, weather_data.back_yard.temp, 'BACK_YARD_TEMP')
	push_temp_isy(ISY_STATE, FRONT_DOOR_TEMP, weather_data.front_door.temp, 'FRONT_DOOR_TEMP')
	push_temp_isy(ISY_STATE, THEATER_WINDOW_TEMP, weather_data.theater_window.temp, 'THEATER_WINDOW_TEMP')
	push_temp_isy(ISY_STATE, MASTER_BEDROOM_TEMP, weather_data.master_bedroom_window.temp, 'MASTER_BEDROOM_TEMP')
	syslog.syslog(syslog.LOG_CRIT, "ISY Temps pushed")


def main():
	weather_data = stations.get_weather()
	update_isy(weather_data)


main()
