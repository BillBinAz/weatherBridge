#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import requests
import syslog

NODES = 'nodes/'

ZW_THEATER_6IN1 = "nodes/ZW047_1"
ZW_LIVING_ROOM_6IN1 = "nodes/ZW048_1"

ZW_KITCHEN_THERMOSTAT = "nodes/n004_t521752427579"
ZW_LIBRARY_ECOBEE = "nodes/n004_rs_ptth"
ZW_GUEST_ECOBEE = "nodes/n004_rs_x9pl"
ZW_KITCHEN_ECOBEE = "nodes/n004_s521752427579"
ZW_CHEESE_ECOBEE = "nodes/n004_rs_x9lx"
ZW_THEATER_ECOBEE = "nodes/n004_rs_bwn4"
ZW_LIVING_ROOM_ECOBEE = "nodes/n004_rs_bw6z"

ZW_MASTER_THERMOSTAT = "nodes/n004_t521778805292"
ZW_GYM_ECOBEE = "nodes/n004_rs_kz2j"
ZW_MASTER_ECOBEE = "nodes/n004_s521778805292"
ZW_OFFICE_ECOBEE = "nodes/n004_rs_f869"

ZW_MAIN_GARAGE = "nodes/ZW025_1"
ZW_MC_GARAGE = "nodes/ZW095_1"
ZW_MAIN_GARAGE_FAN = "nodes/ZW078_1"
ZW_SPA_PUMP = "nodes/ZW044_1"
ZW_POOL_LIGHT = "nodes/ZW080_1"
ALARM_ZONES_CLOSED = "vars/get/2/4"

TEMPERATURE = "ST"
CLIMATE_HEAT_POINT = "CLISPH"
CLIMATE_COOL_POINT = "CLISPC"
CLIMATE_MODE = "CLIMD"
TEMPERATURE_6IN1 = "CLITEMP"
LUX_6IN1 = "LUMIN"
HUMIDITY = "CLIHUM"
OCCUPANCY = "GV1"
HEAT_COOL_STATE = "CLIHCS"  # 0 = idle | 1 = Heat | 2 = Cool

ALARM_STATUS = "nodes/n007_partition1"
ALARM_FRONT_GARAGE_DOOR = "nodes/n007_zone01"
ALARM_SLIDING_GLASS_DOOR = "nodes/n007_zone02"
ALARM_LIVING_GREAT = "nodes/n007_zone03"
ALARM_MASTER = "nodes/n007_zone04"
ALARM_OFFICES = "nodes/n007_zone05"
ALARM_WEST_WING = "nodes/n007_zone06"
ALARM_LIVING_GREAT_MOTION = "nodes/n007_zone07"
ALARM_MASTER_MOTION = "nodes/n007_zone08"
ALARM_BIKE_GARAGE = "nodes/n007_zone10"
ALARM_ARMED = 1
ALARM_DISARMED = 0
ARMED_STARTS_AT = 2
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
		syslog.syslog(syslog.LOG_CRIT, "Bad Data from isy994 " + str(value) + " " + source)
		print(datetime.datetime.now().time(), " -  Bad Data from isy994 " + str(source) + " " + source)
	return formatted_value


def get_node_xml(node, s, user_name, password):

	try:
		# do a get on isy994 to update the data
		url = "http://isy994.evilminions.org/rest/" + str(node)
		ret = s.get(url, auth=(user_name, password), verify=False)
		if ret.status_code != 200:
			syslog.syslog(syslog.LOG_INFO, "Bad response from isy994 " + str(ret.status_code))
			print(datetime.datetime.now().time(), " -  Bad response from isy994. " + str(ret.status_code))
			return
		return xml.etree.ElementTree.fromstring(ret.content.decode())
	except Exception as e:
		syslog.syslog(syslog.LOG_CRIT, "Unable to get isy994 " + str(e))
		print(datetime.datetime.now().time(), "Unable to get isy994 " + str(e))
	return


def get_weather(weather_data):

	try:
		#
		# Get ISY security data
		with open(SECRET_FILE, "r") as secret_file:
			user_name = secret_file.readline().strip('\n')
			password = secret_file.readline().strip('\n')

		s = requests.Session()

		xml_response = get_node_xml(ZW_THEATER_6IN1, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == HUMIDITY:
				weather_data.theater.humidity = sensor.get('value')
			elif sensor.get('id') == LUX_6IN1:
				weather_data.theater.lux = sensor.get('value')
			elif sensor.get('id') == TEMPERATURE_6IN1:
				weather_data.theater.temp = sensor.get('formatted')[:-2]

		xml_response = get_node_xml(ZW_THEATER_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.theater.sensor.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.theater.sensor.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_CHEESE_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.cheese.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.cheese.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_GUEST_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.guest.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.guest.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_KITCHEN_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.kitchen_thermostat.sensor.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.kitchen_thermostat.sensor.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_LIBRARY_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.library.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.library.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_LIVING_ROOM_6IN1, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == HUMIDITY:
				weather_data.living_room.humidity = sensor.get('value')
			elif sensor.get('id') == LUX_6IN1:
				weather_data.living_room.lux = sensor.get('value')
			elif sensor.get('id') == TEMPERATURE_6IN1:
				weather_data.living_room.temp = sensor.get('formatted')[:-2]

		xml_response = get_node_xml(ZW_LIVING_ROOM_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.living_room.sensor.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.living_room.sensor.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_MASTER_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.master_bedroom_thermostat.sensor.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.master_bedroom_thermostat.sensor.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_OFFICE_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.office.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.office.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_GYM_ECOBEE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == TEMPERATURE:
				weather_data.gym.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == OCCUPANCY:
				weather_data.gym.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_KITCHEN_THERMOSTAT, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == CLIMATE_MODE:
				weather_data.kitchen_thermostat.mode = sensor.get('formatted')
			elif sensor.get('id') == TEMPERATURE:
				weather_data.kitchen_thermostat.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == CLIMATE_COOL_POINT:
				weather_data.kitchen_thermostat.cool_set = sensor.get('value')
			elif sensor.get('id') == CLIMATE_HEAT_POINT:
				weather_data.kitchen_thermostat.heat_set = sensor.get('value')
			elif sensor.get('id') == HUMIDITY:
				weather_data.kitchen_thermostat.humidity = sensor.get('value')
			elif sensor.get('id') == HEAT_COOL_STATE:
				weather_data.kitchen_thermostat.state = sensor.get('value')

		xml_response = get_node_xml(ZW_MASTER_THERMOSTAT, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == CLIMATE_MODE:
				weather_data.master_bedroom_thermostat.mode = sensor.get('formatted')
			elif sensor.get('id') == TEMPERATURE:
				weather_data.master_bedroom_thermostat.temp = sensor.get('formatted')[:-2]
			elif sensor.get('id') == CLIMATE_COOL_POINT:
				weather_data.master_bedroom_thermostat.cool_set = sensor.get('value')
			elif sensor.get('id') == CLIMATE_HEAT_POINT:
				weather_data.master_bedroom_thermostat.heat_set = sensor.get('value')
			elif sensor.get('id') == HUMIDITY:
				weather_data.master_bedroom_thermostat.humidity = sensor.get('value')
			elif sensor.get('id') == HEAT_COOL_STATE:
				weather_data.master_bedroom_thermostat.state = sensor.get('value')

		xml_response = get_node_xml(ZW_POOL_LIGHT, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.pool.light = sensor.get('formatted')

		xml_response = get_node_xml(ZW_SPA_PUMP, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.spa.pump = sensor.get('formatted')

		xml_response = get_node_xml(ZW_MAIN_GARAGE_FAN, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.main_garage.fan = sensor.get('formatted')

		xml_response = get_node_xml(ALARM_STATUS, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				if int(sensor.get('value')) >= ARMED_STARTS_AT:
					weather_data.alarm.status = ALARM_ARMED
				else:
					weather_data.alarm.status = ALARM_DISARMED

		xml_response = get_node_xml(ALARM_FRONT_GARAGE_DOOR, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.front_garage_door = sensor.get('value')

		xml_response = get_node_xml(ALARM_SLIDING_GLASS_DOOR, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.sliding_glass_door = sensor.get('value')

		xml_response = get_node_xml(ALARM_LIVING_GREAT, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.living_great = sensor.get('value')

		xml_response = get_node_xml(ALARM_MASTER, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.master = sensor.get('value')

		xml_response = get_node_xml(ALARM_OFFICES, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.offices = sensor.get('value')

		xml_response = get_node_xml(ALARM_WEST_WING, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.west_wing = sensor.get('value')

		xml_response = get_node_xml(ALARM_BIKE_GARAGE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.bike_garage = sensor.get('value')

		xml_response = get_node_xml(ZW_MC_GARAGE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				if sensor.get('value') == "100":
					weather_data.alarm.mc_garage = "1"
				else:
					weather_data.alarm.mc_garage = "0"

		xml_response = get_node_xml(ZW_MAIN_GARAGE, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				if sensor.get('value') == "100":
					weather_data.alarm.main_garage = "1"
				else:
					weather_data.alarm.main_garage = "0"

		s.close()

		weather_data.whole_house_fan.houseTemp = round((float(weather_data.kitchen_thermostat.sensor.temp) +
														float(weather_data.master_bedroom_thermostat.sensor.temp) +
														float(weather_data.office.temp) +
														float(weather_data.gym.temp) +
														float(weather_data.library.temp) +
														float(weather_data.living_room.sensor.temp) +
														float(weather_data.cheese.temp) +
														float(weather_data.guest.temp) +
														float(weather_data.theater.sensor.temp)) / 9.0, 1)

	except Exception as e:
		syslog.syslog(syslog.LOG_CRIT, "Unable to parse isy994 " + str(e))
		print(datetime.datetime.now().time(), "Unable to parse isy994 " + str(e))
	finally:
		return

