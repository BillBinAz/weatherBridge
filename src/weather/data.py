import datetime as dt
import json

DEFAULT_TEMP = 'None'


class Alarm(object):
    def __init__(self):
        self.status = 0
        self.status_label = "None"
        self.great_room_motion = 0
        self.garage_entry_door = 0
        self.guest_bedrooms_bath = 0
        self.great_room_windows = 0
        self.great_room_french_doors = 0
        self.master_bedroom_window = 0
        self.master_bathroom_windows = 0
        self.master_bedroom_motion = 0
        self.front_entry_door = 0
        self.den_window = 0
        self.dining_room_window = 0
        self.back_patio_door = 0

        self.single_garage = 0
        self.double_garage = 0
        self.all_zones_closed = 0


class WholeHomeFan(object):
    def __int__(self):
        self.speed = ""
        self.timeRemaining = ""
        self.cubitFeetPerMinute = ""
        self.power = ""
        self.atticTemp = ""
        self.houseTemp = ""
        self.fan_zones_all = 0
        self.fan_zones_some = 0


class SensorSmall(object):
    def __init__(self):
        self.temp = DEFAULT_TEMP
        self.temp_c = DEFAULT_TEMP
        self.humidity = 0.0


class SensorSmallWithCalibration(object):
    def __init__(self):
        self.temp = DEFAULT_TEMP
        self.temp_raw = DEFAULT_TEMP
        self.temp_calibration = 0.0
        self.temp_c = DEFAULT_TEMP
        self.humidity = 0.0
        self.humidity_raw = 0.0
        self.humidity_calibration = 0.0
        self.time = ""


class Sensor6In1(object):

    def __init__(self):
        self.temp = DEFAULT_TEMP
        self.humidity = 0.0
        self.lux = 0
        self.occupied = 0


class SensorMajor(object):

    def __init__(self):
        self.temp = DEFAULT_TEMP
        self.dew_point = 0.0
        self.humidity = 0.0
        self.wind_direction = ""
        self.wind_speed = 0.0
        self.wind_gust = 0.0
        self.wind_chill = 0.0
        self.pressure = 0
        self.rain_rate = 0.0
        self.rain_total = 0.0


class SensorThermostat(object):

    def __init__(self):
        self.temp = DEFAULT_TEMP
        self.mode = ""
        self.state = 0
        self.humidity = 0.0
        self.heat_set = 0.0
        self.cool_set = 0.0
        self.sensor = EcobeeSensor()

class EcobeeSensor(object):

    def __init__(self):
        self.temp = DEFAULT_TEMP
        self.occupied = 0

class NodeTemp(object):
    def __init__(self):
        self.temp = DEFAULT_TEMP

class NodeTempHumidity(object):
    def __init__(self):
        self.temp = DEFAULT_TEMP
        self.humidity = 0.0

class Locks(object):

    def __init__(self):
        self.locked = 0


class Doors(object):

    def __init__(self):
        self.front_entry_door = Locks()
        self.master_bedroom_entry_door = Locks()
        self.main_garage_side_door = Locks()
        self.main_garage_entry_door = Locks()
        self.bike_garage_entry_door = Locks()


class WeatherData(object):

    def __init__(self):
        # Davis Weather Station
        self.back_yard = SensorMajor()

        # Envisalink
        self.alarm = Alarm()

        # Sensor Push
        self.rack = SensorSmallWithCalibration()

        # Ecobee
        self.hallway_thermostat = SensorThermostat()
        self.bedroom_left = EcobeeSensor()
        self.bedroom_right = EcobeeSensor()
        self.living_room = EcobeeSensor()
        self.master_bedroom = EcobeeSensor()
        self.office = EcobeeSensor()

        # Node
        self.humidor = NodeTempHumidity()
        self.safe = NodeTempHumidity()
        self.garage = NodeTemp()
        self.garage_freezer = NodeTemp()
        self.kitchen = NodeTemp()
        self.kitchen_refrigerator = NodeTemp()
        self.kitchen_freezer = NodeTemp()

        # Airscape
        self.whole_house_fan = WholeHomeFan()
        self.date_generated = dt.datetime.now().strftime("%m-%d-%y %I:%M %p")

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
