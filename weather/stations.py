#!/usr/bin/python3
from rtl_433 import weather433
from stations import isy994, kiosk, meteohub, airScape
from weather import data


def get_weather():
	cur_weather = data.WeatherData()
	cur_weather = isy994.get_weather(cur_weather)
	cur_weather = meteohub.get_weather(cur_weather)
	cur_weather = weather433.get_weather(cur_weather)
	cur_weather = kiosk.get_weather(cur_weather)
	cur_weather = airScape.get_weather(cur_weather)
	return cur_weather


def main():
	cur_weather = get_weather()


# print(cur_weather.to_json())


main()
