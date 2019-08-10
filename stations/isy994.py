#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import httplib2
import syslog

from weather import data
NODES = 'nodes/'

ZW_THEATER_6IN1 = "nodes/ZW047_1"
ZW_LIVING_ROOM_6IN1 = "nodes/ZW048_1"
ZW_LIVING_ROOM_ECOBEE = "nodes/n001_ecobee1_sen3"
ZW_THEATER_ECOBEE = "nodes/n001_ecobee1_sen2"
ZW_KITCHEN_THERMOSTAT = "nodes/n001_ecobee1"
ZW_MASTER_THERMOSTAT = "nodes/n001_ecobee2"

ZW_THEATER_FAN = "nodes/ZW041_1"
ZW_LIVING_FAN = "nodes/ZW042_1"
ZW_MASTER_FAN = "nodes/ZW043_1"
ZW_LIBRARY_FAN = "nodes/ZW034_1"
ZW_OFFICE_FAN = "nodes/ZW033_1"
ZW_MAIN_GARAGE = "nodes/ZW025_1"
ZW_MC_GARAGE = "nodes/ZW049_1"
ZW_SPA_PUMP = "nodes/ZW044_1"
ZW_POOL_LIGHT = "nodes/ZW071_1"
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
SECRET_FILE = "./secret/isy994"


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def format_f(value, source):
	#
	# add decimal place
	formatted_value = 0
	try:
		formatted_value = round(float(value) / 10.0, 1)
	except:
		syslog.syslog(syslog.LOG_INFO, "Bad Data from isy994 " + str(value) + " " + source)
		print(datetime.datetime.now().time(), " -  Bad Data from isy994 " + str(source) + " " + source)
	return formatted_value


def get_node_xml(node):
	#
	# Get ISY security data
	with open(SECRET_FILE, "r") as secret_file:
		user_name = secret_file.readline().strip('\n')
		password = secret_file.readline().strip('\n')

	#
	# do a get on isy994 to update the data
	url = "http://isy994.evilminions.org/rest/" + str(node)
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h.request(url, "GET")
	if resp.status != 200:
		syslog.syslog(syslog.LOG_INFO, "Bad response from isy994 " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from isy994. " + str(resp))
	xml_response = xml.etree.ElementTree.fromstring(content)
	return xml_response


def get_weather(weather_data):

	try:
		xml_response = get_node_xml(ZW_THEATER_6IN1)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == HUMIDITY_6IN1:
				weather_data.theater.humidity = sensor.get('value')
			elif sensor.get('id') == LUX_6IN1:
				weather_data.theater.lux = sensor.get('value')

		xml_response = get_node_xml(ZW_THEATER_ECOBEE)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.theater.temp = sensor.get('formatted')[:-1]

		xml_response = get_node_xml(ZW_LIVING_ROOM_6IN1)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == HUMIDITY_6IN1:
				weather_data.living_room.humidity = sensor.get('value')
			elif sensor.get('id') == LUX_6IN1:
				weather_data.living_room.lux = sensor.get('value')

		xml_response = get_node_xml(ZW_LIVING_ROOM_ECOBEE)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.living_room.temp = sensor.get('formatted')[:-1]

		xml_response = get_node_xml(ZW_KITCHEN_THERMOSTAT)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == CLIMATE_MODE:
				weather_data.kitchen_thermostat.mode = sensor.get('formatted')
			elif sensor.get('id') == TEMPERATURE:
				weather_data.kitchen_thermostat.temp = sensor.get('formatted')[:-1]
			elif sensor.get('id') == CLIMATE_COOL_POINT:
				weather_data.kitchen_thermostat.cool_set = sensor.get('value')
			elif sensor.get('id') == CLIMATE_HEAT_POINT:
				weather_data.kitchen_thermostat.heat_set = sensor.get('value')

		xml_response = get_node_xml(ZW_MASTER_THERMOSTAT)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == CLIMATE_MODE:
				weather_data.master_bedroom_thermostat.mode = sensor.get('formatted')
			elif sensor.get('id') == TEMPERATURE:
				weather_data.master_bedroom_thermostat.temp = sensor.get('formatted')[:-1]
			elif sensor.get('id') == CLIMATE_COOL_POINT:
				weather_data.master_bedroom_thermostat.cool_set = sensor.get('value')
			elif sensor.get('id') == CLIMATE_HEAT_POINT:
				weather_data.master_bedroom_thermostat.heat_set = sensor.get('value')

		xml_response = get_node_xml(ZW_POOL_LIGHT)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.pool.light = sensor.get('formatted')

		xml_response = get_node_xml(ZW_SPA_PUMP)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.spa.pump = sensor.get('formatted')

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
				weather_data.alarm.status = sensor.get('value')

		xml_response = get_node_xml(ALARM_FRONT_GARAGE_DOOR)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.front_garage_door = sensor.get('value')

		xml_response = get_node_xml(ALARM_SLIDING_GLASS_DOOR)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.sliding_glass_door = sensor.get('value')

		xml_response = get_node_xml(ALARM_LIVING_GREAT)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.living_great = sensor.get('value')

		xml_response = get_node_xml(ALARM_MASTER)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.master = sensor.get('value')

		xml_response = get_node_xml(ALARM_OFFICES)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.offices = sensor.get('value')

		xml_response = get_node_xml(ALARM_WEST_WING)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.west_wing = sensor.get('value')

		xml_response = get_node_xml(ALARM_BIKE_GARAGE)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.bike_garage = sensor.get('value')

		xml_response = get_node_xml(ZW_MC_GARAGE)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				if sensor.get('value') == "100":
					weather_data.alarm.mc_garage = "1"
				else:
					weather_data.alarm.mc_garage = "0"

		xml_response = get_node_xml(ZW_MAIN_GARAGE)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				if sensor.get('value') == "100":
					weather_data.alarm.main_garage = "1"
				else:
					weather_data.alarm.main_garage = "0"
	except xml.etree.ElementTree.ParseError as e:
		syslog.syslog(syslog.LOG_INFO, "Unable to parse isy994 " + e.msg)
		print(datetime.datetime.now().time(), "Unable to parse isy994 " + e.msg)
	finally:
		return weather_data


def main():
	weather_data = data.WeatherData()
	get_weather(weather_data)


# print(cur_weather.to_json())


main()
