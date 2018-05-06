import json

from dataclasses import dataclass


@dataclass
class SensorSmall(object):

	def __init__(self):
		self.temp = 0.0
		self.humidity = 0.0


class Sensor6In1(object):

	def __init__(self):
		self.temp = 0.0
		self.humidity = 0.0
		self.lux = 0


class SensorMajor(object):

	def __init__(self):
		self.temp = 0.0
		self.dew_point = 0.0
		self.humidity = 0.0
		self.wind_direction = ""
		self.wind_speed = 0.0
		self.wind_gust = 0.0
		self.wind_chill = 0.0
		self.pressure = 0
		self.rain_rate = 0.0
		self.rain_total = 0.0


@dataclass
class SensorThermostat(object):

	def __init__(self):
		self.temp = 0.0
		self.mode = ""
		self.heat_set = 0.0
		self.cool_set = 0.0


@dataclass
class WeatherData(object):

	def __init__(self):
		self.theater_window = SensorSmall()
		self.theater = Sensor6In1()
		self.back_yard = SensorMajor()
		self.master_bedroom_window = SensorSmall()
		self.library = SensorSmall()
		self.humidor = SensorSmall()
		self.front_door = SensorSmall()
		self.living_room = Sensor6In1()
		self.master_bedroom_thermostat = SensorThermostat()
		self.kitchen_thermostat = SensorThermostat()
		self.front_yard = SensorSmall()

	def to_json(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
