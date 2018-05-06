#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import httplib2
import syslog

from weather import data

ZW_THEATER_6IN1 = "ZW047_1"
ZW_LIVING_ROOM_6IN1 = "ZW048_1"
ZW_KITCHEN_THERMOSTAT = "ZW011_1"
ZW_MASTER_THERMOSTAT = "ZW012_1"

ZW_THEATER_FAN = "ZW041_1"
ZW_LIVING_FAN = "ZW042_1"
ZW_MASTER_FAN = "ZW043_1"
ZW_LIBRARY_FAN = "ZW034_1"
ZW_OFFICE_FAN = "ZW033_1"

TEMPERATURE = "ST"
CLIMATE_HEAT_POINT = "CLISPH"
CLIMATE_COOL_POINT = "CLISPC"
CLIMATE_MODE = "CLIMD"
TEMPERATURE_6IN1 = "CLITEMP"
LUX_6IN1 = "LUMIN"
HUMIDITY_6IN1 = "CLIHUM"


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def format_f(value):
	#
	# add decimal place
	return round(float(value) / 10, 1)


def get_node_xml(node):
	#
	# Get ISY security data
	secret_file = open("./secret/isy994", "r")
	user_name = secret_file.readline().strip('\n')
	password = secret_file.readline().strip('\n')

	#
	# do a get on isy994 to update the data
	url = "http://isy994.evilminions.org/rest/nodes/" + str(node)
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h.request(url, "GET")
	if resp.status != 200:
		syslog.syslog(syslog.LOG_EMERG, "Bad response from meteohub " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from meteohub." + str(resp))
	xml_response = xml.etree.ElementTree.fromstring(content)
	return xml_response


def get_weather(weather_data):
	xml_response = get_node_xml(ZW_THEATER_6IN1)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == HUMIDITY_6IN1:
			weather_data.theater.humidity = sensor.get('value')
		elif sensor.get('id') == TEMPERATURE_6IN1:
			weather_data.theater.temp = format_f(sensor.get('value'))
		elif sensor.get('id') == LUX_6IN1:
			weather_data.theater.lux = sensor.get('value')

	xml_response = get_node_xml(ZW_LIVING_ROOM_6IN1)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == HUMIDITY_6IN1:
			weather_data.living_room.humidity = sensor.get('value')
		elif sensor.get('id') == TEMPERATURE_6IN1:
			weather_data.living_room.temp = format_f(sensor.get('value'))
		elif sensor.get('id') == LUX_6IN1:
			weather_data.living_room.lux = sensor.get('value')

	xml_response = get_node_xml(ZW_KITCHEN_THERMOSTAT)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == CLIMATE_MODE:
			weather_data.kitchen_thermostat.mode = sensor.get('formatted')
		elif sensor.get('id') == TEMPERATURE:
			weather_data.kitchen_thermostat.temp = format_f(sensor.get('value'))
		elif sensor.get('id') == CLIMATE_COOL_POINT:
			weather_data.kitchen_thermostat.cool_set = format_f(sensor.get('value'))
		elif sensor.get('id') == CLIMATE_HEAT_POINT:
			weather_data.kitchen_thermostat.heat_set = format_f(sensor.get('value'))

	xml_response = get_node_xml(ZW_MASTER_THERMOSTAT)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == CLIMATE_MODE:
			weather_data.master_bedroom_thermostat.mode = sensor.get('formatted')
		elif sensor.get('id') == TEMPERATURE:
			weather_data.master_bedroom_thermostat.temp = format_f(sensor.get('value'))
		elif sensor.get('id') == CLIMATE_COOL_POINT:
			weather_data.master_bedroom_thermostat.cool_set = format_f(sensor.get('value'))
		elif sensor.get('id') == CLIMATE_HEAT_POINT:
			weather_data.master_bedroom_thermostat.heat_set = format_f(sensor.get('value'))

	xml_response = get_node_xml(ZW_THEATER_FAN)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.theater_window.fan = sensor.get('formatted')

	xml_response = get_node_xml(ZW_LIVING_FAN)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.living_room.fan = sensor.get('formatted')

	xml_response = get_node_xml(ZW_MASTER_FAN)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.master_bedroom_window.fan = sensor.get('formatted')

	xml_response = get_node_xml(ZW_LIBRARY_FAN)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.library.fan = sensor.get('formatted')

	xml_response = get_node_xml(ZW_OFFICE_FAN)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.front_door.fan = sensor.get('formatted')

	return weather_data


def main():
	weather_data = data.WeatherData()
	get_weather(weather_data)


main()
