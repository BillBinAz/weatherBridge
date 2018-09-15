#!/usr/bin/python3
import isy994
import meteohub
from rtl_433 import weather433
import get_rest_rtl_433
from weather import data


def get_weather():
	cur_weather = data.WeatherData()
	cur_weather = get_rest_rtl_433.get_weather(cur_weather)
	cur_weather = isy994.get_weather(cur_weather)
	cur_weather = meteohub.get_weather(cur_weather)
	cur_weather = weather433.get_weather(cur_weather)
	return cur_weather


def main():
	get_weather()


main()
