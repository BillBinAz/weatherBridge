#!/usr/bin/python3
import datetime as dt
import requests
import logging
import json
import utilities.connect as connect
import utilities.conversions as conversions

CONNECT_ITEM_ID = "r6menry2h3yxd7nrfjgop7oktu"
HOME_ASSISTANT_URL = "https://home-assistant.evilminions.org:8123/api/states/"
ENTITY_ID_OFFICE_TEMPERATURE = "sensor.bills_office_temperature"
ENTITY_ID_OFFICE_OCCUPANCY = "binary_sensor.bills_office_occupancy"
ENTITY_ID_LEFT_BEDROOM_TEMPERATURE = "sensor.ambers_office_temperature"
ENTITY_ID_LEFT_BEDROOM_OCCUPANCY = "binary_sensor.ambers_office_occupancy"
ENTITY_ID_RIGHT_BEDROOM_TEMPERATURE = "sensor.cheese_room_temperature"
ENTITY_ID_RIGHT_BEDROOM_OCCUPANCY = "binary_sensor.cheese_room_occupancy"
ENTITY_ID_LIVING_ROOM_TEMPERATURE = "sensor.great_room_temperature"
ENTITY_ID_LIVING_ROOM_OCCUPANCY = "binary_sensor.great_room_occupancy"
ENTITY_ID_MASTER_BEDROOM_TEMPERATURE = "sensor.master_bedroom_temperature"
ENTITY_ID_MASTER_BEDROOM_OCCUPANCY = "binary_sensor.master_bedroom_occupancy"
ENTITY_ID_HALLWAY_TEMPERATURE = "sensor.shotgun_temperature"
ENTITY_ID_HALLWAY_OCCUPANCY = "binary_sensor.shotgun_occupancy"
ENTITY_ID_HALLWAY_HUMIDITY = "sensor.shotgun_humidity"
ENTITY_ID_HALLWAY_THERMOSTAT = "climate.shotgun"
ENTITY_ID_GARAGE_SINGLE = "binary_sensor.garagedoorsingle_sensor_state_any"
ENTITY_ID_GARAGE_DOUBLE = "binary_sensor.garagedoorsingle_sensor_state_any"
ENTITY_ID_HUMIDOR_TEMPERATURE = "sensor.humidorsensor_air_temperature"
ENTITY_ID_HUMIDOR_HUMIDITY = "sensor.humidorsensor_humidity"
ENTITY_ID_SAFE_TEMPERATURE = "sensor.safesensor_air_temperature"
ENTITY_ID_SAFE_HUMIDITY = "sensor.safesensor_humidity"
ENTITY_ID_SAFE_MOTION = "binary_sensor.safesensor_sensor_state_any"
ENTITY_ID_SAFE_LUX = "sensor.safesensor_illuminance"


ENTITY_ID_ALARM_GARAGE = "binary_sensor.garage_entry_door"
ENTITY_ID_ALARM_GUEST_BEDROOMS = "binary_sensor.guest_bedrooms_and_bath"
ENTITY_ID_ALARM_GREAT_ROOM_WINDOWS = "binary_sensor.great_room_windows"
ENTITY_ID_ALARM_MASTER_BEDROOM_WINDOWS = "binary_sensor.master_bedroom_window"
ENTITY_ID_ALARM_GREAT_ROOM_FRENCH_DOORS = "binary_sensor.great_room_french_doors"
ENTITY_ID_ALARM_MASTER_BATHROOM_WINDOWS = "binary_sensor.master_bathroom_windows"
ENTITY_ID_ALARM_FRONT_ENTRY_DOOR = "binary_sensor.front_entry_door"
ENTITY_ID_ALARM_DEN = "binary_sensor.den"
ENTITY_ID_ALARM_DINING_ROOM = "binary_sensor.dining_room_window"
ENTITY_ID_ALARM_BACK_PATIO_DOOR = "binary_sensor.back_patio_door"
ENTITY_ID_ALARM_GREAT_ROOM_MOTION = "binary_sensor.great_room_motion"
ENTITY_ID_ALARM_MASTER_BEDROOM_MOTION = "binary_sensor.master_bedroom_motion"
ENTITY_ID_ALARM_STATUS_LABEL = "sensor.home_alarm_keypad"
ENTITY_ID_ALARM_STATUS = "alarm_control_panel.home_alarm"


def get_bearer_token():
    try:
        #
        # Get security data
        credentials = connect.get_credentials(CONNECT_ITEM_ID)
        return credentials[0].value

    except Exception as e:
        logging.error("Unable to get home-assistant:get_bearer_token " + str(e))
        print(dt.datetime.now().time(), "Unable to home-assistant:get_bearer_token " + str(e))
    return


def get_sensor_data(bearer_token, key, s):
    try:
        url = HOME_ASSISTANT_URL + key
        ret = s.get(url, headers={"Accept": "application/json", "Authorization": "Bearer " + bearer_token})

        if ret.status_code != 200:
            logging.error("Bad response from home-assistant " + str(ret.status_code))
            print(dt.datetime.now().time(), " -  Bad response from home-assistant. " + str(ret.status_code))
            raise Exception("Bad response from home-assistant " + str(ret.status_code))

        response = json.loads(ret.content.decode())
        if not response:
            raise Exception("No Data from home-assistant:SensorData.")

        return response

    except Exception as e:
        logging.error("Unable to get home-assistant:get_sensor_data " + str(e))
        print(dt.datetime.now().time(), "Unable to get home-assistant:get_sensor_data " + url + str(e))
    return


def get_temperature(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    return sensor_data["state"]


def get_occupancy(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] == "on":
        return 1
    else:
        return 0


def get_garage_door(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] == "off":
        return 1
    else:
        return 0


def get_zone_status(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] == "off":
        return 1
    else:
        return 0


def get_alarm_label(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return ""
    label = sensor_data["state"]
    label = label.replace("*", "")
    return label[:10].title().strip()


def get_alarm_status(bearer_token, key, s):
    sensor_data = get_sensor_data(bearer_token, key, s)
    if sensor_data is None:
        return 0
    if sensor_data["state"] != "disarmed":
        return 1
    else:
        return 0


def get_alarm_data(weather_data, bearer_token, s):
    weather_data.alarm.back_patio_door = get_zone_status(bearer_token, ENTITY_ID_ALARM_BACK_PATIO_DOOR, s)
    weather_data.alarm.den_window = get_zone_status(bearer_token, ENTITY_ID_ALARM_DEN, s)
    weather_data.alarm.dining_room_window = get_zone_status(bearer_token, ENTITY_ID_ALARM_DINING_ROOM, s)
    weather_data.alarm.front_entry_door = get_zone_status(bearer_token, ENTITY_ID_ALARM_FRONT_ENTRY_DOOR, s)
    weather_data.alarm.garage_entry_door = get_zone_status(bearer_token, ENTITY_ID_ALARM_GARAGE, s)
    weather_data.alarm.great_room_french_doors = get_zone_status(bearer_token,
                                                                 ENTITY_ID_ALARM_GREAT_ROOM_FRENCH_DOORS, s)
    weather_data.alarm.great_room_motion = get_zone_status(bearer_token, ENTITY_ID_ALARM_GREAT_ROOM_WINDOWS, s)
    weather_data.alarm.great_room_motion = get_zone_status(bearer_token, ENTITY_ID_ALARM_GREAT_ROOM_MOTION, s)
    weather_data.alarm.great_room_windows = get_zone_status(bearer_token, ENTITY_ID_ALARM_GREAT_ROOM_WINDOWS, s)
    weather_data.alarm.guest_bedrooms_bath = get_zone_status(bearer_token, ENTITY_ID_ALARM_GUEST_BEDROOMS, s)
    weather_data.alarm.master_bathroom_windows = get_zone_status(bearer_token,
                                                                 ENTITY_ID_ALARM_MASTER_BATHROOM_WINDOWS, s)
    weather_data.alarm.master_bedroom_motion = get_zone_status(bearer_token,
                                                               ENTITY_ID_ALARM_MASTER_BEDROOM_MOTION, s)
    weather_data.alarm.master_bedroom_window = get_zone_status(bearer_token,
                                                               ENTITY_ID_ALARM_MASTER_BEDROOM_WINDOWS, s)
    weather_data.alarm.status_label = get_alarm_label(bearer_token, ENTITY_ID_ALARM_STATUS_LABEL, s)
    weather_data.alarm.status = get_alarm_status(bearer_token, ENTITY_ID_ALARM_STATUS, s)


def get_thermostat_data(weather_data, bearer_token, s):

    sensor_data = get_sensor_data(bearer_token, ENTITY_ID_HALLWAY_THERMOSTAT, s)

    weather_data.hallway_thermostat.heat_set = sensor_data["attributes"]["target_temp_low"]
    weather_data.hallway_thermostat.cool_set = sensor_data["attributes"]["target_temp_high"]
    weather_data.hallway_thermostat.humidity = sensor_data["attributes"]["current_humidity"]
    weather_data.hallway_thermostat.fan = sensor_data["attributes"]["fan_mode"][:10].title().strip()
    weather_data.hallway_thermostat.temp = sensor_data["attributes"]["current_temperature"]
    weather_data.hallway_thermostat.state = sensor_data["attributes"]["hvac_action"][:10].title().strip()

    mode = sensor_data["attributes"]["preset_mode"]
    if sensor_data is None:
        return
    if sensor_data["state"] == "off":
        weather_data.hallway_thermostat.mode = "Off"
    elif mode == "temp":
        weather_data.hallway_thermostat.mode = "Override"
    else:
        weather_data.hallway_thermostat.mode = mode[:10].title().strip()


def get_weather(weather_data):

    s = requests.Session()

    try:
        bearer_token = get_bearer_token()
        if not bearer_token:
            raise Exception("No Data from home-assistant:BearerToken.")
        #
        # Get Office
        weather_data.office.temp = get_temperature(bearer_token, ENTITY_ID_OFFICE_TEMPERATURE, s)
        weather_data.office.occupied = get_occupancy(bearer_token, ENTITY_ID_OFFICE_OCCUPANCY, s)

        # Get Left Bedroom
        weather_data.bedroom_left.temp = get_temperature(bearer_token, ENTITY_ID_LEFT_BEDROOM_TEMPERATURE, s)
        weather_data.bedroom_left.occupied = get_occupancy(bearer_token, ENTITY_ID_LEFT_BEDROOM_OCCUPANCY, s)

        # Get Right Bedroom
        weather_data.bedroom_right.temp = get_temperature(bearer_token, ENTITY_ID_RIGHT_BEDROOM_TEMPERATURE, s)
        weather_data.bedroom_right.occupied = get_occupancy(bearer_token, ENTITY_ID_RIGHT_BEDROOM_OCCUPANCY, s)

        # Get Living Room
        weather_data.living_room.temp = get_temperature(bearer_token, ENTITY_ID_LIVING_ROOM_TEMPERATURE, s)
        weather_data.living_room.occupied = get_occupancy(bearer_token, ENTITY_ID_LIVING_ROOM_OCCUPANCY, s)

        # Get Master Bedroom
        weather_data.master_bedroom.temp = get_temperature(bearer_token, ENTITY_ID_MASTER_BEDROOM_TEMPERATURE, s)
        weather_data.master_bedroom.occupied = get_occupancy(bearer_token, ENTITY_ID_MASTER_BEDROOM_OCCUPANCY, s)

        # Humidor Humidity
        weather_data.humidor.humidity = get_temperature(bearer_token, ENTITY_ID_HUMIDOR_HUMIDITY, s)
        weather_data.humidor.temp = get_temperature(bearer_token, ENTITY_ID_HUMIDOR_TEMPERATURE, s)

        # Safe Humidity
        weather_data.safe.humidity = get_temperature(bearer_token, ENTITY_ID_SAFE_HUMIDITY, s)
        weather_data.safe.temp = get_temperature(bearer_token, ENTITY_ID_SAFE_TEMPERATURE, s)
        weather_data.safe.occupied = get_occupancy(bearer_token, ENTITY_ID_SAFE_MOTION, s)
        weather_data.safe.lux = get_temperature(bearer_token, ENTITY_ID_SAFE_LUX, s)

        # Get Hallway
        weather_data.hallway_thermostat.sensor.temp = get_temperature(bearer_token, ENTITY_ID_HALLWAY_TEMPERATURE, s)
        weather_data.hallway_thermostat.sensor.occupied = get_occupancy(bearer_token, ENTITY_ID_HALLWAY_OCCUPANCY, s)

        # Get Garage
        weather_data.alarm.single_garage = get_garage_door(bearer_token, ENTITY_ID_GARAGE_SINGLE, s)
        weather_data.alarm.double_garage = get_garage_door(bearer_token, ENTITY_ID_GARAGE_DOUBLE, s)

        # get Thermostat
        get_thermostat_data(weather_data, bearer_token, s)

        # Get Alarm
        get_alarm_data(weather_data, bearer_token, s)

    except Exception as e:
        logging.error("Unable to get home-assistant:get_weather " + str(e))
        print(dt.datetime.now().time(), "Unable to get home-assistant:get_weather " + str(e))
    finally:
        s.close()
    return
