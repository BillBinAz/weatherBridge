#!/usr/bin/python3

import datetime
import xml.etree.ElementTree

import httplib2
import syslog

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
	url = "http://isy994/rest/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(f_temp)
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h.request(url, "GET")
	if not str(content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
		syslog.syslog(syslog.LOG_EMERG, "Failed URL: " + url + " Response: " + str(content))
		print(datetime.datetime.now().time(), " - Failed URL: ", url, " Response: ", str(content))
	else:
		print(datetime.datetime.now().time(), " - Success URL: ", url)


def c_to_f(c_temp):
	#
	# Convert from celsius to fahrenheit
	return round(9.0 / 5.0 * float(c_temp) + 32)


def get_meteobridge_xml():
	#
	# Get the username/password from the secret file
	secret_file = open("./secret/meteobridge", "r")
	user_name = secret_file.readline().strip('\n')
	password = secret_file.readline().strip('\n')

	#
	# Pull the XML from meteobridge
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h. \
		request("http://meteobridge/cgi-bin/livedataxml.cgi", "GET")
	if resp.status != 200:
		syslog.syslog(syslog.LOG_EMERG, "Bad response from meteobridge " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from meteobridge." + str(resp))
	xml_response = xml.etree.ElementTree.fromstring(content)
	return xml_response


def update_isy_meteobridge():

	#
	# Process the XML Variables
	meteobridge_xml = get_meteobridge_xml()
	for sensor in meteobridge_xml.findall('TH'):
		if sensor.get('id') == "th6":
			push_temp_isy(ISY_STATE, FRONT_DOOR_TEMP, c_to_f(sensor.get('temp')))
		elif sensor.get('id') == "th7":
			push_temp_isy(ISY_STATE, THEATER_WINDOW_TEMP, c_to_f(sensor.get('temp')))
		elif sensor.get('id') == "th8":
			push_temp_isy(ISY_STATE, MASTER_BEDROOM_TEMP, c_to_f(sensor.get('temp')))
	syslog.syslog(syslog.LOG_CRIT, "Meteobridge data pushed.")


def get_meteohub_xml():
	#
	# get the last 5 minutes worth of data
	date = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)
	url = "http://meteohub/meteolog.cgi?type=xml&quotes=1&mode=data&start=" + date.strftime("%Y%m%d%H%M%S")

	#
	# Pull the XML from meteobridge
	h = httplib2.Http()
	resp, content = h.request(url, "GET")
	if resp.status != 200:
		syslog.syslog(syslog.LOG_EMERG, "Bad response from meteohub " + str(resp))
		print(datetime.datetime.now().time(), " -  Bad response from meteohub." + str(resp))
	xml_response = xml.etree.ElementTree.fromstring(content)
	return xml_response


def update_isy_meteohub():
	meteohub_xml = get_meteohub_xml()
	for sensor in meteohub_xml.findall('TH'):
		if sensor.get('id') == "th0":
			temp = sensor.get('temp')
	push_temp_isy(ISY_STATE, BACK_YARD_TEMP, c_to_f(temp))
	syslog.syslog(syslog.LOG_CRIT, "Meteohub data pushed.")


def main():
	update_isy_meteobridge()
	update_isy_meteohub()


main()
