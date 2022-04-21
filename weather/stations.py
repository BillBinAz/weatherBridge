#!/usr/bin/python3
from stations import isy994, rtl433, airScape, wifiLogger, sensorPush
from weather import data


def get_weather():
	cur_weather = data.WeatherData()
	isy994.get_weather(cur_weather)
	wifiLogger.get_weather(cur_weather)
	airScape.get_weather(cur_weather)
	rtl433.get_weather(cur_weather, "humidor-pi.evilminions.org")
	rtl433.get_weather(cur_weather, "rtl433.evilminions.org")
	sensorPush.get_weather(cur_weather)
	return cur_weather
