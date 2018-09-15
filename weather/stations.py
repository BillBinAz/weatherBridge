#!/usr/bin/python3
import station_isy994
import station_kiosk
import station_meteohub
from rtl_433 import weather433
from weather import data


def get_weather():
	cur_weather = data.WeatherData()
	cur_weather = station_isy994.get_weather(cur_weather)
	cur_weather = station_meteohub.get_weather(cur_weather)
	cur_weather = weather433.get_weather(cur_weather)
	cur_weather = station_kiosk.get_weather(cur_weather)
	return cur_weather


def main():
	cur_weather = get_weather()


# print(cur_weather.to_json())


main()
