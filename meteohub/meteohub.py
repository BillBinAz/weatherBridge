#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import httplib2
import syslog

from weather import data

TEMPERATURE_NODE = "TH"
BACK_YARD_TEMP_ID = "th0"
WIND_NODE = "WIND"
BACK_YARD_WIND_ID = "wind0"
RAIN_NODE = "RAIN"
BACK_YARD_RAIN_ID = "rain0"
POOL_TEMP_ID = "th1"
SPA_TEMP_ID = "th2"
CONTROLLER_NODE = "THB"
CONTROLLER_ID = "thb0"
S_OK = 200

TEMPERATURE = 'temp'
HUMIDITY = 'hum'
DEP_POINT = 'dew'
RAIN_RATE = 'rate'
RAIN_TOTAL = 'total'
WIND_DIRECTION = 'dir'
WIND_GUST = 'gust'
WIND_SPEED = 'wind'
WIND_CHILL = 'chill'
PRESSURE = 'press'


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


def get_meteohub_xml():
	#
	# get the last 5 minutes worth of data
	date = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
	url = "http://meteohub/meteolog.cgi?type=xml&quotes=1&mode=data&start=" + date.strftime("%Y%m%d%H%M%S")

	#
	# Pull the XML from meteohub
	h = httplib2.Http()
	resp, content = h.request(url, "GET")
	if resp.status != 200:
		syslog.syslog(syslog.LOG_EMERG, "Bad response from meteohub " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from meteohub. " + str(resp))
	xml_response = xml.etree.ElementTree.fromstring(content)
	return xml_response


def get_weather(weather_data):
	meteohub_xml = get_meteohub_xml()
	last_sensor = None

	# Temperature - Back yard
	for sensor in meteohub_xml.findall(TEMPERATURE_NODE):
		if sensor.get('id') == BACK_YARD_TEMP_ID:
			last_sensor = sensor
	weather_data.back_yard.temp = c_to_f(last_sensor.get(TEMPERATURE))
	weather_data.back_yard.humidity = last_sensor.get(HUMIDITY)
	weather_data.back_yard.dew_point = c_to_f(last_sensor.get(DEP_POINT))

	# Rain
	for sensor in meteohub_xml.findall(RAIN_NODE):
		if sensor.get('id') == BACK_YARD_RAIN_ID:
			last_sensor = sensor
	weather_data.back_yard.rain_rate = mm_to_inches(last_sensor.get(RAIN_RATE))
	weather_data.back_yard.rain_total = mm_to_inches(last_sensor.get(RAIN_TOTAL))

	# Wind
	for sensor in meteohub_xml.findall(WIND_NODE):
		if sensor.get('id') == BACK_YARD_WIND_ID:
			last_sensor = sensor
	weather_data.back_yard.wind_speed = mps_to_mph(last_sensor.get(WIND_SPEED))
	weather_data.back_yard.wind_gust = mps_to_mph(last_sensor.get(WIND_GUST))
	weather_data.back_yard.wind_direction = deg_to_compass(last_sensor.get(WIND_DIRECTION))
	weather_data.back_yard.wind_chill = last_sensor.get(WIND_CHILL)

	# Pressure
	for sensor in meteohub_xml.findall(CONTROLLER_NODE):
		if sensor.get('id') == CONTROLLER_ID:
			last_sensor = sensor
	weather_data.back_yard.pressure = last_sensor.get(PRESSURE)

	# Temperature - Spa
	for sensor in meteohub_xml.findall(TEMPERATURE_NODE):
		if sensor.get('id') == SPA_TEMP_ID:
			last_sensor = sensor
	weather_data.spa.temp = c_to_f(last_sensor.get(TEMPERATURE))

	# Temperature - Pool
	for sensor in meteohub_xml.findall(TEMPERATURE_NODE):
		if sensor.get('id') == POOL_TEMP_ID:
			last_sensor = sensor
	weather_data.pool.temp = c_to_f(last_sensor.get(TEMPERATURE))

	return weather_data


def main():
	cur_weather = data.WeatherData()
	get_weather(cur_weather)


main()
