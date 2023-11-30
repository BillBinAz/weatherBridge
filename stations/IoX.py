#!/usr/bin/python3

import datetime
import xml.etree.ElementTree
import requests
import logging
import sys
import Utilities.connect as connect

NODES = 'nodes/'
ERROR_XML = '<?xml version="1.0" encoding="UTF-8"?><nodeInfo><node/><properties/></nodeInfo>'
URL = "http://polisy.evilminions.org:8080/rest/"

ZW_HALLWAY_THERMOSTAT = "nodes/n001_t531695453465"
ZW_HALLWAY_THERMOSTAT_SENSOR = "nodes/n001_s531695453465"
ZW_BEDROOM_LEFT = "nodes/n001_rs_ldtb"
ZW_BEDROOM_RIGHT = "nodes/n001_rs_8lzm"
ZW_LIVING_ROOM = "nodes/n001_rs_lzs4"
ZW_MASTER_BEDROOM = "nodes/n001_rs_lvf5"
ZW_OFFICE = "nodes/n001_rs_l2dq"
ZW_GARAGE_SINGLE = "nodes/ZY139_1"
ZW_GARAGE_DOUBLE = "nodes/ZY049_1"

TEMPERATURE = "ST"
LOCK_STATUS = "ST"
LOCKED = "Locked"
CLIMATE_HEAT_POINT = "CLISPH"
CLIMATE_COOL_POINT = "CLISPC"
CLIMATE_MODE = "CLIMD"
TEMPERATURE_6IN1 = "CLITEMP"
LUX_6IN1 = "LUMIN"
HUMIDITY = "CLIHUM"
OCCUPANCY = "GV1"
HEAT_COOL_STATE = "CLIHCS"  # 0 = idle | 1 = Heat | 2 = Cool
CONNECT_ITEM_ID = "ymulwralgldqemmer2bx4exr3q"


def get_node_xml(node, s, user_name, password):

	try:
		# do a get on IoX to update the data
		url = URL + str(node)
		ret = s.get(url, auth=(user_name, password), verify=False)
		if ret.status_code != 200:
			raise Exception(f'Bad response from IoX:{str(ret.status_code)} {url}')
		return xml.etree.ElementTree.fromstring(ret.content.decode())
	except Exception as e:
		logging.error(str(e))
		print(datetime.datetime.now().time(), str(e))
	return


def get_weather(weather_data):

	s = requests.Session()

	try:
		#
		# Get security data
		credentials = connect.get_credentials(CONNECT_ITEM_ID)
		user_name = credentials[0].value
		password = credentials[1].value

		xml_response = get_node_xml(ZW_BEDROOM_LEFT, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					weather_data.bedroom_left.temp = sensor.get('formatted')[:-2]
				elif sensor.get('id') == OCCUPANCY:
					weather_data.bedroom_left.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_BEDROOM_RIGHT, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					weather_data.bedroom_right.temp = sensor.get('formatted')[:-2]
				elif sensor.get('id') == OCCUPANCY:
					weather_data.bedroom_right.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_LIVING_ROOM, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					weather_data.living_room.temp = sensor.get('formatted')[:-2]
				elif sensor.get('id') == OCCUPANCY:
					weather_data.living_room.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_MASTER_BEDROOM, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					weather_data.master_bedroom.temp = sensor.get('formatted')[:-2]
				elif sensor.get('id') == OCCUPANCY:
					weather_data.master_bedroom.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_OFFICE, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					weather_data.office.temp = sensor.get('formatted')[:-2]
				elif sensor.get('id') == OCCUPANCY:
					weather_data.office.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_HALLWAY_THERMOSTAT_SENSOR, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					weather_data.hallway_thermostat.sensor.temp = sensor.get('formatted')[:-2]
				elif sensor.get('id') == OCCUPANCY:
					weather_data.hallway_thermostat.sensor.occupied = sensor.get('value')

		xml_response = get_node_xml(ZW_HALLWAY_THERMOSTAT, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == CLIMATE_MODE:
					weather_data.hallway_thermostat.mode = sensor.get('formatted')
				elif sensor.get('id') == TEMPERATURE:
					weather_data.hallway_thermostat.temp = sensor.get('formatted')[:-2]
				elif sensor.get('id') == CLIMATE_COOL_POINT:
					weather_data.hallway_thermostat.cool_set = sensor.get('value')
				elif sensor.get('id') == CLIMATE_HEAT_POINT:
					weather_data.hallway_thermostat.heat_set = sensor.get('value')
				elif sensor.get('id') == HUMIDITY:
					weather_data.hallway_thermostat.humidity = sensor.get('value')
				elif sensor.get('id') == HEAT_COOL_STATE:
					weather_data.hallway_thermostat.state = sensor.get('value')

		xml_response = get_node_xml(ZW_GARAGE_SINGLE, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					if sensor.get('formatted') == 'Off':
						weather_data.alarm.single_garage = 1
					else:
						weather_data.alarm.single_garage = 0

		xml_response = get_node_xml(ZW_GARAGE_DOUBLE, s, user_name, password)
		if xml_response:
			for sensor in xml_response.find('properties').findall('property'):
				if sensor.get('id') == TEMPERATURE:
					if sensor.get('formatted') == 'Off':
						weather_data.alarm.double_garage = 1
					else:
						weather_data.alarm.double_garage = 0

		weather_data.whole_house_fan.houseTemp = round((float(weather_data.hallway_thermostat.sensor.temp) +
														float(weather_data.bedroom_left.temp) +
														float(weather_data.bedroom_right.temp) +
														float(weather_data.living_room.temp) +
														float(weather_data.living_room.temp) +
														float(weather_data.master_bedroom.temp) +
														float(weather_data.office.temp) ) / 7.0, 1)

	except Exception as e:
		logging.error("Unable to get IoX:get_weather " + str(e))
		print(datetime.datetime.now().time(), "Unable to get IoX:get_weather " + str(e))
	finally:
		s.close()
		e = sys.exc_info()[0]
		if e:
			logging.error("Unable to get IoX:get_weather " + str(e))
			print(datetime.datetime.now().time(), "Unable to get IoX:get_weather " + str(e))
	return


