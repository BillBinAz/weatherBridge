#!/usr/bin/python3

from isy994 import isy994
from meteohub import meteohub
from rtl_433 import weather433
from weather import data


def get_weather():
	cur_weather = data.WeatherData()
	cur_weather = isy994.get_weather(cur_weather)
	cur_weather = meteohub.get_weather(cur_weather)
	cur_weather = weather433.get_weather(cur_weather)
	return cur_weather


def main():
	get_weather()


main()
