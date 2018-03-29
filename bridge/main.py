import xml.etree.ElementTree

import httplib2


def push_temp(variable_type, variable_id, c_temp):
	f_temp = round(9.0 / 5.0 * float(c_temp) + 32, 2)
	http_object = httplib2.Http()
	http_object.add_credentials(user_mame, password)  # Basic authentication
	resp, meteo_content = http_object. \
		request("http://meteobridge/cgi-bin/livedataxml.cgi", "GET")

	print(c_temp, f_temp)


#
# Get the username/password from the secret file
secret_file = open("../secret/meteobridge", "r")
user_mame = secret_file.readline().strip('\n')
password = secret_file.readline().strip('\n')

#
# Pull the XML from meteobridge
http_object = httplib2.Http()
http_object.add_credentials(user_mame, password)  # Basic authentication
resp, meteo_content = http_object. \
	request("http://meteobridge/cgi-bin/livedataxml.cgi", "GET")

#
# Process the XML Variables
meteobridge_xml = xml.etree.ElementTree.fromstring(meteo_content)
for sensor in meteobridge_xml.findall('TH'):
	if sensor.get('id') == "th6":
		push_temp(2, 1, sensor.get('temp'))
	elif sensor.get('id') == "th0":
		push_temp(2, 2, sensor.get('temp'))
	elif sensor.get('id') == "th7":
		push_temp(2, 5, sensor.get('temp'))
	elif sensor.get('id') == "th8":
		push_temp(2, 12, sensor.get('temp'))
