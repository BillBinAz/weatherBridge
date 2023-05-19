#!/usr/bin/python3
from stations import IoX, airScape, wifiLogger, sensorPush, myq, evisalink4_alarm
from weather import data
import datetime
import logging
import sys


def get_weather():

	cur_weather = data.WeatherData()

	try:
		logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S:%f', level=logging.INFO)

		cur_weather = data.WeatherData()
		IoX.get_weather(cur_weather)
		wifiLogger.get_weather(cur_weather)
		airScape.get_weather(cur_weather)
		# rtl433.get_weather(cur_weather, "rtl433.evilminions.org")
		myq.get_weather(cur_weather)
		sensorPush.get_weather(cur_weather)
		evisalink4_alarm.get_weather(cur_weather)

	except Exception as e:
		logging.error("Unable to get station:get_weather " + str(e))
		print(datetime.datetime.now().time(), "Unable to get station:get_weather " + str(e))
	except:
		e = sys.exc_info()[0]
		logging.error("Unable to get station:get_weather " + str(e))
		print(datetime.datetime.now().time(), "Unable to get station:get_weather " + str(e))

	return cur_weather
