#!/usr/bin/python3

from weather import data
from weather import isy994
from weather import meteobridge
from weather import meteohub


def get_weather():
	cur_weather = data.WeatherData()
	cur_weather = isy994.get_weather(cur_weather)
	cur_weather = meteohub.get_weather(cur_weather)
	cur_weather = meteobridge.get_weather(cur_weather)

	return cur_weather


def main():
	get_weather()


main()
