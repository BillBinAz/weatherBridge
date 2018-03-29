import xml.etree.ElementTree

import httplib2


def push_temp_isy(variable_type, variable_id, c_temp):
	#
	# Convert from celsius to fahrenheit
	f_temp = round(9.0 / 5.0 * float(c_temp) + 32)
	url = "http://isy994/rest/vars/set/" + str(variable_type) + "/" + str(variable_id) + "/" + str(f_temp)

	#
	# Get ISY security data
	secret_file = open("../secret/isy994", "r")
	user_name = secret_file.readline().strip('\n')
	password = secret_file.readline().strip('\n')

	#
	# do a get on isy994 to update the data
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h.request(url, "GET")
	if not str(content).find("<RestResponse succeeded=\"true\"><status>200</status></RestResponse>"):
		print("Failed URL: ", url, "Response: ", content)


def get_meteobridge_xml():
	#
	# Get the username/password from the secret file
	secret_file = open("../secret/meteobridge", "r")
	user_name = secret_file.readline().strip('\n')
	password = secret_file.readline().strip('\n')

	#
	# Pull the XML from meteobridge
	h = httplib2.Http()
	h.add_credentials(user_name, password)  # Basic authentication
	resp, content = h. \
		request("http://meteobridge/cgi-bin/livedataxml.cgi", "GET")
	xml_response = xml.etree.ElementTree.fromstring(content)
	return xml_response


def update_isy_meteobridge():
	#
	# Process the XML Variables
	meteobridge_xml = get_meteobridge_xml()
	for sensor in meteobridge_xml.findall('TH'):
		if sensor.get('id') == "th6":
			push_temp_isy(2, 1, sensor.get('temp'))
		elif sensor.get('id') == "th0":
			push_temp_isy(2, 2, sensor.get('temp'))
		elif sensor.get('id') == "th7":
			push_temp_isy(2, 5, sensor.get('temp'))
		elif sensor.get('id') == "th8":
			push_temp_isy(2, 12, sensor.get('temp'))
	print("Meteobridge data pushed")


def main():
	update_isy_meteobridge()


main()
