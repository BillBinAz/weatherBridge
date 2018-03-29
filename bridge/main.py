import xml.etree.ElementTree

import httplib2

#
# Get the username/password from the secret file
secretFile = open("../secret/meteobridge", "r")
userName = secretFile.readline().strip('\n')
password = secretFile.readline().strip('\n')

#
# Pull the XML from meteobridge
httpObject = httplib2.Http()
httpObject.add_credentials(userName, password)  # Basic authentication
resp, meteoContent = httpObject. \
  request("http://meteobridge/cgi-bin/livedataxml.cgi", "GET")

#
# Process the XML Variables
meteoHubXML = xml.etree.ElementTree.parse(meteoContent).getroot()

