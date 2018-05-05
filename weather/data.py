from dataclasses import dataclass


@dataclass
class SensorSmall(object):
	temp: float
	humidity: float

	def __init__(self):
		self.temp = 0.0
		self.humidity = 0.0


class Sensor6In1(object):
	temp: float
	humidity: float
	lux: int

	def __init__(self):
		self.temp = 0.0
		self.humidity = 0.0
		self.lux = 0


class SensorMajor(object):
	temp: float
	dew_point: float
	humidity: float
	wind_direction: str
	wind_speed: float
	wind_gust: float
	wind_chill: float
	pressure: int
	rain_rate: float
	rain_total: float

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
	temp: float
	mode: str
	heat_set: float
	cool_set: float

	def __init__(self):
		self.temp = 0.0
		self.mode = ""
		self.heat_set = 0.0
		self.cool_set = 0.0


@dataclass
class WeatherData(object):
	theater_window: SensorSmall
	theater: Sensor6In1
	back_yard: SensorMajor
	master_bedroom_window: SensorSmall
	library: SensorSmall
	humidor: SensorSmall
	front_door: SensorSmall
	living_room: Sensor6In1
	front_yard: SensorSmall
	master_bedroom_thermostat: SensorThermostat
	kitchen_thermostat: SensorThermostat

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
