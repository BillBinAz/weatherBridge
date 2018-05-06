#!/usr/bin/python3

import datetime

import httplib2
import syslog

from weather import stations

ISY_STATE = 2
FRONT_DOOR_TEMP = 1
BACK_YARD_TEMP = 2
THEATER_WINDOW_TEMP = 5
MASTER_BEDROOM_TEMP = 12


def push_temp_isy(variable_type, variable_id, f_temp):
	#
	# Get ISY security data
	secret_file = open("./secret/isy994", "r")
	user_name = secret_file.readline().strip('\n')
	password = secret_file.readline().strip('\n')

	#
	# do a get on isy994 to update the data
	url = "http://isy994/rest/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(round(f_temp))
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h.request(url, "GET")
	if not str(content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
		syslog.syslog(syslog.LOG_EMERG, "Failed URL: " + url + " Response: " + str(content))
		print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(content))
	else:
		print(datetime.datetime.now().time(), " - Success URL: ", url)


def update_isy(weather_data):
	push_temp_isy(ISY_STATE, BACK_YARD_TEMP, weather_data.back_yard.temp)
	push_temp_isy(ISY_STATE, FRONT_DOOR_TEMP, weather_data.front_door.temp)
	push_temp_isy(ISY_STATE, THEATER_WINDOW_TEMP, weather_data.theater_window.temp)
	push_temp_isy(ISY_STATE, MASTER_BEDROOM_TEMP, weather_data.master_bedroom_window.temp)
	syslog.syslog(syslog.LOG_CRIT, "ISY Temps pushed")


def main():
	weather_data = stations.get_weather()
	update_isy(weather_data)


main()
