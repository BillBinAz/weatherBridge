#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import requests
import logging


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32, 1)


def format_f(value, source):
	#
	# add decimal place
	formatted_value = 0
	try:
		formatted_value = round(float(value), 2)
	except:
		logging.error("Bad Data from AirScape " + str(value) + " " + source)
		print(datetime.datetime.now().time(), " -  Bad Data from AirScape " + str(source) + " " + source)
	return formatted_value


def get_node_xml():

	try:
		url = "http://fan.evilminions.org/status.xml.cgi"
		ret = requests.post(url, verify=False)
		ret.close()
		if ret.status_code != 200:
			logging.error("Bad response from AirScape " + str(ret.status_code))
			print(datetime.datetime.now().time(), " -  Bad response from AirScape. " + str(ret.status_code))
			return
		return xml.etree.ElementTree.fromstring(clean_up_xml(ret.content))
	except Exception as e:
		logging.error("Unable to parse AirScape " + str(e))
		print(datetime.datetime.now().time(), "Unable to parse AirScape " + str(e))
	return


def clean_up_xml(content):
	try:
		str_content = content.decode("utf=8", "ignore")
		start = str_content.find("<server_response>")
		end = str_content.find("</server_response>") + len("</server_response>")
		return str_content.replace(str_content[start:end], "").replace("\n", "")
	except Exception as e:
		logging.error("Unable to get AirScape " + str(e))
		print(datetime.datetime.now().time(), "Unable to get AirScape " + str(e))
	return


# 	<?xml version="1.0" encoding="UTF-8"?>
# 	<airscapewhf>
# 		<fanspd>0</fanspd>
# 		<doorinprocess>0</doorinprocess>
# 		<timeremaining>0</timeremaining>
# 		<macaddr>60:CB:FB:00:80:3F</macaddr>
# 		<ipaddr>192.168.0.23</ipaddr>
# 		<model>5300 WHF</model>
# 		<softver>2.17.1</softver>
# 		<interlock1>0</interlock1>
# 		<cfm>0</cfm>
# 		<power>0</power>
# 		<house_temp>-99</house_temp>
# 		<DNS1>192.168.0.1</DNS1>
# 		<attic_temp>102</attic_temp>
# 		<oa_temp>-99</oa_temp>
# 		<server_response>��$�޻@j2a�e0������|�</server_response>
# 		<DIPS>11110</DIPS>
# 		<switch2>1111</switch2>
# 		<Setpoint>0</Setpoint>
# 	</airscapewhf>

def get_weather(weather_data):

	try:
		xml_response = get_node_xml()
		weather_data.whole_house_fan.atticTemp = xml_response.find('attic_temp').text
		weather_data.whole_house_fan.speed = xml_response.find('fanspd').text
		weather_data.whole_house_fan.cubitFeetPerMinute = xml_response.find('cfm').text
		weather_data.whole_house_fan.power = xml_response.find('power').text
		hours = int(xml_response.find('timeremaining').text) / 60
		weather_data.whole_house_fan.timeRemaining = format_f(hours, 'timeremaining')
	except xml.etree.ElementTree.ParseError as e:
		logging.error("Unable to parse AirScape " + e.msg)
		print(datetime.datetime.now().time(), "Unable to parse AirScape " + e.msg)
	finally:
		return

