#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import httplib2
import syslog

from weather import data

ZW_THEATER_6IN1 = "nodes/ZW047_1"
ZW_LIVING_ROOM_6IN1 = "nodes/ZW048_1"
ZW_KITCHEN_THERMOSTAT = "nodes/ZW011_1"
ZW_MASTER_THERMOSTAT = "nodes/ZW012_1"

ZW_THEATER_FAN = "nodes/ZW041_1"
ZW_LIVING_FAN = "nodes/ZW042_1"
ZW_MASTER_FAN = "nodes/ZW043_1"
ZW_LIBRARY_FAN = "nodes/ZW034_1"
ZW_OFFICE_FAN = "nodes/ZW033_1"
ZW_MAIN_GARAGE = "nodes/ZW025_1"
ZW_MC_GARAGE = "nodes/ZW049_1"

ALARM_ZONES_CLOSED = "vars/get/2/4"

TEMPERATURE = "ST"
CLIMATE_HEAT_POINT = "CLISPH"
CLIMATE_COOL_POINT = "CLISPC"
CLIMATE_MODE = "CLIMD"
TEMPERATURE_6IN1 = "CLITEMP"
LUX_6IN1 = "LUMIN"
HUMIDITY_6IN1 = "CLIHUM"

ALARM_STATUS = "nodes/n001_hwalrm1_part1"
ALARM_ALL_ZONES = "vars/get/2/4"
ALARM_FRONT_GARAGE_DOOR = "nodes/n001_hwalrm1_z01"
ALARM_SLIDING_GLASS_DOOR = "nodes/n001_hwalrm1_z02"
ALARM_LIVING_GREAT = "nodes/n001_hwalrm1_z03"
ALARM_MASTER = "nodes/n001_hwalrm1_z04"
ALARM_OFFICES = "nodes/n001_hwalrm1_z05"
ALARM_WEST_WING = "nodes/n001_hwalrm1_z06"
ALARM_LIVING_GREAT_MOTION = "nodes/n001_hwalrm1_z07"
ALARM_MASTER_MOTION = "nodes/n001_hwalrm1_z08"
ALARM_BIKE_GARAGE = "nodes/n001_hwalrm1_z10"


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def format_f(value):
	#
	# add decimal place
	return round(float(value) / 10.0, 1)


def get_node_xml(node):
	#
	# Get ISY security data
	secret_file = open("./secret/isy994", "r")
	user_name = secret_file.readline().strip('\n')
	password = secret_file.readline().strip('\n')

	#
	# do a get on isy994 to update the data
	url = "http://isy994.evilminions.org/rest/" + str(node)
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

	xml_response = get_node_xml(ALARM_STATUS)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.status = sensor.get('formatted')

	xml_response = get_node_xml(ALARM_FRONT_GARAGE_DOOR)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.front_garage_door = sensor.get('formatted')

	xml_response = get_node_xml(ALARM_SLIDING_GLASS_DOOR)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.sliding_glass_door = sensor.get('formatted')

	xml_response = get_node_xml(ALARM_LIVING_GREAT)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.living_great = sensor.get('formatted')

	xml_response = get_node_xml(ALARM_MASTER)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.master = sensor.get('formatted')

	xml_response = get_node_xml(ALARM_OFFICES)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.offices = sensor.get('formatted')

	xml_response = get_node_xml(ALARM_WEST_WING)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.west_wing = sensor.get('formatted')

	xml_response = get_node_xml(ALARM_BIKE_GARAGE)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			weather_data.alarm.bike_garage = sensor.get('formatted')

	xml_response = get_node_xml(ZW_MC_GARAGE)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			if sensor.get('value') == "100":
				weather_data.alarm.mc_garage = "0"
			else:
				weather_data.alarm.mc_garage = "1"

	xml_response = get_node_xml(ZW_MAIN_GARAGE)
	for sensor in xml_response.find('properties').findall('property'):
		if sensor.get('id') == 'ST':
			if sensor.get('value') == "100":
				weather_data.alarm.mc_garage = "0"
			else:
				weather_data.alarm.mc_garage = "1"

	# All Zones Closed Variable
	# xml_response = get_node_xml(ALARM_ZONES_CLOSED)
	# weather_data.alarm.all_zones = xml_response.find('val').text

	return weather_data


def main():
	weather_data = data.WeatherData()
	get_weather(weather_data)


main()
