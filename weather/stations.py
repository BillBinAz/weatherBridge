#!/usr/bin/python3
from rtl_433 import weather433
from stations import isy994, rtl433, airScape, wifiLogger
from weather import data


def get_weather():
	cur_weather = data.WeatherData()
	cur_weather = isy994.get_weather(cur_weather)
	cur_weather = wifiLogger.get_weather(cur_weather)
	cur_weather = airScape.get_weather(cur_weather)
	cur_weather = rtl433.get_weather(cur_weather, "kiosk.evilminions.org")
	cur_weather = rtl433.get_weather(cur_weather, "cairo.evilminions.org")
	return cur_weather
