#!/usr/bin/python3
from stations import isy994, rtl433, airScape, wifiLogger, sensorPush, myq
from weather import data
import logging


def get_weather():

	logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s', datefmt='%Y-%m-%d,%H:%M:%S:%f', level=logging.INFO)

	cur_weather = data.WeatherData()
	isy994.get_weather(cur_weather)
	wifiLogger.get_weather(cur_weather)
	airScape.get_weather(cur_weather)
	rtl433.get_weather(cur_weather, "rtl433.evilminions.org")
	myq.get_weather(cur_weather)
	sensorPush.get_weather(cur_weather)
	return cur_weather
