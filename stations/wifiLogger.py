#!/usr/bin/python3

import datetime
import json

import httplib2
import syslog

from weather import data

S_OK = 200
TEMPERATURE_OUTDOOR = 'tempout'
LEAF_TEMP = 'xlt'
HUMIDITY_OUTDOOR = 'humout'
DEP_POINT = 'dew'
RAIN_RATE = 'rainr'
RAIN_24_HOURS = 'rain24'
WIND_DIRECTION = 'winddir'
WIND_GUST = 'gust'
WIND_SPEED = 'windspd'
WIND_CHILL = 'chill'
PRESSURE = 'bar'


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def mps_to_mph(mps):
	#
	# Convert from meters per second to miles per hour
	return round(2.2369 * float(mps), 1)


def mm_to_inches(mm):
	#
	# convert from mm to inches
	return round(float(mm) * 0.0393700787, 2)


def deg_to_compass(direction):
	#
	# degrees to compass direction
	compass = ""
	degrees = float(direction)

	if (degrees >= 0) and (degrees < 11.25):
		compass = " N "
	elif (degrees >= 11.25) and (degrees < 33.75):
		compass = "NNE"
	elif (degrees >= 33.75) and (degrees < 56.25):
		compass = " NE"
	elif (degrees >= 56.25) and (degrees < 78.75):
		compass = "ENE"
	elif (degrees >= 78.75) and (degrees < 101.25):
		compass = " E "
	elif (degrees >= 101.25) and (degrees < 123.75):
		compass = "ESE"
	elif (degrees >= 123.75) and (degrees < 146.25):
		compass = " SE"
	elif (degrees >= 146.25) and (degrees < 168.75):
		compass = "SSE"
	elif (degrees >= 168.75) and (degrees < 191.25):
		compass = " S "
	elif (degrees >= 191.25) and (degrees < 213.75):
		compass = "SSW"
	elif (degrees >= 213.75) and (degrees < 236.25):
		compass = " SW"
	elif (degrees >= 236.25) and (degrees < 258.75):
		compass = "WSW"
	elif (degrees >= 258.75) and (degrees < 281.25):
		compass = " W "
	elif (degrees >= 281.25) and (degrees < 303.75):
		compass = "WNW"
	elif (degrees >= 303.75) and (degrees < 326.25):
		compass = " NW"
	elif (degrees >= 326.25) and (degrees < 348.75):
		compass = "NNW"
	elif degrees >= 348.75:
		compass = " N "

	return compass


def get_data():
	#
	# get the last 5 minutes worth of data
	url = "http://wifilogger.evilminions.org/wflexp.json"

	#
	# Pull the data
	h = httplib2.Http()
	resp, content = h.request(url, "GET")
	if resp.status != 200:
		syslog.syslog(syslog.LOG_INFO, "Bad response from wifilogger " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from wifilogger. " + str(resp))
	return json.loads(content)


def get_weather(weather_data):
	wifi_logger_data = get_data()

	# Temperature - Back yard
	weather_data.back_yard.temp = wifi_logger_data[TEMPERATURE_OUTDOOR]
	weather_data.back_yard.humidity = wifi_logger_data[HUMIDITY_OUTDOOR]
	weather_data.back_yard.dew_point = wifi_logger_data[DEP_POINT]

	# Rain
	weather_data.back_yard.rain_rate = round(float(wifi_logger_data[RAIN_RATE]), 2)
	weather_data.back_yard.rain_total = round(float(wifi_logger_data[RAIN_24_HOURS]), 2)

	# Wind
	weather_data.back_yard.wind_speed = wifi_logger_data[WIND_SPEED]
	weather_data.back_yard.wind_gust = wifi_logger_data[WIND_GUST]
	weather_data.back_yard.wind_direction = deg_to_compass(wifi_logger_data[WIND_DIRECTION])
	weather_data.back_yard.wind_chill = wifi_logger_data[WIND_CHILL]

	# Pressure
	weather_data.back_yard.pressure = wifi_logger_data[PRESSURE]

	# Temperature - Spa
	weather_data.spa.temp = wifi_logger_data[LEAF_TEMP][1]

	# Temperature - Pool
	weather_data.pool.temp = wifi_logger_data[LEAF_TEMP][0]

	return weather_data


def main():
	cur_weather = data.WeatherData()
	# get_weather(cur_weather)
	# print(cur_weather.to_json())


main()
