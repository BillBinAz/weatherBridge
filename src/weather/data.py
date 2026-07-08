import copy
import datetime as dt
import json

DEFAULT_TEMPERATURE = 'None'
ZONE_TYPE_CONTACT = 0
ZONE_TYPE_MOTION = 1
ZONE_TYPE_DOOR = 2
ZONE_TYPE_GARAGE_DOOR = 3
ZONE_TYPE_BASIC = 12
CLIMATE_TYPE_DAVIS = 4
CLIMATE_TYPE_ECOBEE_THERMOSTAT= 5
CLIMATE_TYPE_ECOBEE_SENSOR = 6               # _occupancy _temperature
CLIMATE_TYPE_THERMOWORKS_NODE = 7               # _air_temperature
CLIMATE_TYPE_THERMOWORKS_NODE_WITH_HUMIDITY = 8 # _humidity _air_temperature
CLIMATE_TYPE_THERMOWORKS_NODE_TWO_CHANNEL = 9
CLIMATE_TYPE_SENSOR_PUSH = 10
CLIMATE_TYPE_HUMIDITY = 11


class AlarmZone(object):
    def __init__(self, config):
        # type|zone_id|HA_ID|Label|(optional)
        result = config.split('|')
        self.type = int(result[0])
        self.id = int(result[1])
        self.key = str(result[2])
        self.label = str(result[3])
        if result.__len__() > 4:
            self.door_key = str(result[4])
            self.locked = 0
        self.closed = 0

class Alarm(object):
    def __init__(self):
        self.zones = []
        self.all_zones_closed = 0
        self.status_value = 0
        self.status_label = "None"

class Climate(object):
    def __init__(self):
        self.home_average_temperature = 0.0
        self.sensors = []

    def to_json(self):
        # convert dictionary to named list based on label remove
        return json.dumps({sensor.label: sensor.__dict__ for sensor in self.sensors})

    def create_sensor(self, config):
        result = config.split('|')
        sensor_type = int(result[0])
        if sensor_type == CLIMATE_TYPE_DAVIS:
            return SensorDavisWeatherStation(config)
        elif sensor_type == CLIMATE_TYPE_ECOBEE_THERMOSTAT:
            return SensorEcobeeThermostat(config)
        elif sensor_type == CLIMATE_TYPE_ECOBEE_SENSOR:
            return SensorEcobee(config)
        elif sensor_type == CLIMATE_TYPE_THERMOWORKS_NODE:
            return SensorThermoworksNode(config)
        elif sensor_type == CLIMATE_TYPE_THERMOWORKS_NODE_WITH_HUMIDITY:
            return SensorThermoworksNodeWithHumidity(config)
        elif sensor_type == CLIMATE_TYPE_THERMOWORKS_NODE_TWO_CHANNEL:
            return SensorThermoworksNodeTwoProbes(config)
        elif sensor_type == CLIMATE_TYPE_SENSOR_PUSH:
            return SensorPush(config)
        elif sensor_type == CLIMATE_TYPE_HUMIDITY:
            return SensorHumidifier(config)
        else:
            raise ValueError("Unknown sensor type")

class SensorSmall(object):
    def __init__(self,config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.temperature_c = DEFAULT_TEMPERATURE
        self.humidity = 0.0

class SensorHumidifier(object):
    def __init__(self,config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.mode = "off"
        self.humidity_set = 0.0
        self.humidity = 0.0

class SensorPush(object):
    def __init__(self, config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.temperature_raw = DEFAULT_TEMPERATURE
        self.temperature_calibration = 0.0
        self.temperature_c = DEFAULT_TEMPERATURE
        self.humidity = 0.0
        self.humidity_raw = 0.0
        self.humidity_calibration = 0.0
        self.time = ""

class SensorDavisWeatherStation(object):

    def __init__(self, config):
        result = config.split('|')
        self.type = int(result[0])
        self.label = str(result[1])
        self.url = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.dew_point = 0.0
        self.humidity = 0.0
        self.wind_direction = ""
        self.wind_speed = 0.0
        self.wind_gust = 0.0
        self.wind_chill = 0.0
        self.pressure = 0
        self.rain_rate = 0.0
        self.rain_total = 0.0


class SensorEcobeeThermostat(object):
    def __init__(self, config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.mode = ""
        self.state = 0
        self.humidity = 0.0
        self.heat_set = 0.0
        self.cool_set = 0.0
        self.occupied = 0

class SensorEcobee(object):

    def __init__(self, config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.occupied = 0

class SensorThermoworksNode(object):
    def __init__(self, config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.temperature_probe_0  = DEFAULT_TEMPERATURE

class SensorThermoworksNodeWithHumidity(object):
    def __init__(self, config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.humidity = 0.0

class SensorThermoworksNodeTwoProbes(object):
    def __init__(self, config):
        result = config.split('|')
        self.type = int(result[0])
        self.key = str(result[1])
        self.label = str(result[2])
        self.temperature = DEFAULT_TEMPERATURE
        self.temperature_probe_0  = DEFAULT_TEMPERATURE
        self.temperature_probe_1  = DEFAULT_TEMPERATURE

class Door(object):
    def __init__(self):
        self.label = "None"
        self.locked = 0

class Home(object):
    def __init__(self):
        self.alarm = Alarm()
        self.climate = Climate()
        self.doors = []
        self.date_generated = dt.datetime.now().strftime("%m-%d-%y %I:%M %p")

    def to_json(self):
        self.climate.sensors.sort(key=lambda x: x.label)
        self.alarm.zones.sort(key=lambda x: x.label)
        self.doors.sort(key=lambda x: x.label)

        return json.dumps({
            "alarm": {
                "all_zones_closed": self.alarm.all_zones_closed,
                "status_value": self.alarm.status_value,
                "status_label": self.alarm.status_label,
                "zones": [{zone.label: zone.__dict__} for zone in self.alarm.zones]
            },
            "climate": {
                "home_average_temperature": self.climate.home_average_temperature,
                "sensors": [{sensor.label: sensor.__dict__} for sensor in self.climate.sensors]
            },
            "doors": [{door.label: door.__dict__} for door in self.doors],
            "date_generated": self.date_generated
        })
