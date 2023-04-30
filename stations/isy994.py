#!/usr/bin/python3

import datetime
import xml.etree.ElementTree
import requests
import logging

NODES = 'nodes/'
ERROR_XML = '<?xml version="1.0" encoding="UTF-8"?><nodeInfo><node/><properties/></nodeInfo>'
ZW_THEATER_6IN1 = "nodes/ZW047_1"
ZW_LIVING_ROOM_6IN1 = "nodes/ZW048_1"
ISY_URL = "http://isy994.evilminions.org/rest/"
ZW_KITCHEN_THERMOSTAT = "nodes/n001_t521752427579"
ZW_LIBRARY_ECOBEE = "nodes/n001_rs_ptth"
ZW_GUEST_ECOBEE = "nodes/n001_rs_x9pl"
ZW_KITCHEN_ECOBEE = "nodes/n001_t521752427579"
ZW_CHEESE_ECOBEE = "nodes/n001_rs_x9lx"
ZW_THEATER_ECOBEE = "nodes/n001_rs_bwn4"
ZW_LIVING_ROOM_ECOBEE = "nodes/n001_rs_bw6z"

ZW_MASTER_THERMOSTAT = "nodes/n001_t521778805292"
ZW_GYM_ECOBEE = "nodes/n001_rs_kz2j"
ZW_MASTER_ECOBEE = "nodes/n001_rs_gbfs"
ZW_OFFICE_ECOBEE = "nodes/n001_rs_f869"
ZW_MAIN_GARAGE_FAN = "nodes/ZW078_1"
ZW_SPA_PUMP = "nodes/ZW044_1"
ZW_POOL_LIGHT = "nodes/ZW080_1"
ALARM_ZONES_CLOSED = "vars/get/2/4"

MYQ_MAIN_GARAGE = "nodes/n001_gw33001391fd"
MYQ_MC_GARAGE = "nodes/n001_cg0846887726"
MYQ_BIKE_GARAGE = "nodes/n001_cg08469920f5"

TEMPERATURE = "ST"
CLIMATE_HEAT_POINT = "CLISPH"
CLIMATE_COOL_POINT = "CLISPC"
CLIMATE_MODE = "CLIMD"
TEMPERATURE_6IN1 = "CLITEMP"
LUX_6IN1 = "LUMIN"
HUMIDITY = "CLIHUM"
OCCUPANCY = "GV1"
HEAT_COOL_STATE = "CLIHCS"  # 0 = idle | 1 = Heat | 2 = Cool

ALARM_STATUS = "nodes/n008_hwalrm1_part1"
ALARM_FRONT_GARAGE_DOOR = "nodes/n008_hwalrm1_z01"
ALARM_SLIDING_GLASS_DOOR = "nodes/n008_hwalrm1_z02"
ALARM_LIVING_GREAT = "nodes/n008_hwalrm1_z03"
ALARM_MASTER = "nodes/n008_hwalrm1_z04"
ALARM_OFFICES = "nodes/n008_hwalrm1_z05"
ALARM_WEST_WING = "nodes/n008_hwalrm1_z06"
ALARM_LIVING_GREAT_MOTION = "nodes/n008_hwalrm1_z07"
ALARM_MASTER_MOTION = "nodes/n008_hwalrm1_z08"
ALARM_READY = "Ready"
ALARM_DISARMED = "Disarmed"
ALARM_NOT_READY = "Not Ready"
ALARM_ARMED_AWAY = "Armed Away"
ALARM_ARMED_STAY = "Armed Stay"
ALARM_ARMED_INSTANT = "Armed Instant"
ALARM_ARMED_NIGHT = "Night Armed"
ALARM_ALARMING = "Alarming"
SECRET_FILE = "./secret/isy994"


def get_node_xml(node, s, user_name, password):

	try:
		# do a get on isy994 to update the data
		url = ISY_URL + str(node)
		ret = s.get(url, auth=(user_name, password), verify=False)
		if ret.status_code != 200:
			logging.error("Bad response from isy994 " + str(ret.status_code))
			print(datetime.datetime.now().time(), " -  Bad response from isy994. " + str(ret.status_code))
			return xml.etree.ElementTree.fromstring(ERROR_XML)
		return xml.etree.ElementTree.fromstring(ret.content.decode())
	except Exception as e:
		logging.error("Unable to get isy994 " + str(e))
		print(datetime.datetime.now().time(), "Unable to get isy994 " + str(e))
	return


def get_zone_status(zone_status):

	if str(zone_status) == ALARM_ZONES_CLOSED:
		return 1
	return 0


def get_alarm_status(alarm_status):

	if str(alarm_status) != ALARM_DISARMED:
		return 1
	return 0


def get_weather(weather_data):

	try:
		#
		# Get ISY security data

		with open(SECRET_FILE, "r") as secret_file:
			user_name = secret_file.readline().strip('\n')
			password = secret_file.readline().strip('\n')

		s = requests.Session()

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
				weather_data.alarm.status = get_alarm_status(sensor.get('formatted'))

		xml_response = get_node_xml(ALARM_FRONT_GARAGE_DOOR, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.front_garage_door = get_zone_status(sensor.get('value'))

		xml_response = get_node_xml(ALARM_SLIDING_GLASS_DOOR, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.sliding_glass_door = get_zone_status(sensor.get('value'))

		xml_response = get_node_xml(ALARM_LIVING_GREAT, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.living_great = get_zone_status(sensor.get('value'))

		xml_response = get_node_xml(ALARM_MASTER, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.master = get_zone_status(sensor.get('value'))

		xml_response = get_node_xml(ALARM_OFFICES, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.offices = get_zone_status(sensor.get('value'))

		xml_response = get_node_xml(ALARM_WEST_WING, s, user_name, password)
		for sensor in xml_response.find('properties').findall('property'):
			if sensor.get('id') == 'ST':
				weather_data.alarm.west_wing = get_zone_status(sensor.get('value'))

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
		logging.error("Unable to parse isy994 " + str(e))
		print(datetime.datetime.now().time(), "Unable to parse isy994 " + str(e))
	finally:
		return

