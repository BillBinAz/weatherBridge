#!/usr/bin/python3
import datetime as dt
import json
import logging
import os
import traceback

import requests
from pycognito import Cognito

import utilities.connect as connect
from weather.data import CLIMATE_TYPE_APRILAIRE

logger = logging.getLogger(__name__)

ACCOUNT_URL = "https://account.aprilaire.io/user"
DEVICE_URL = "https://device.aprilaire.io"
COGNITO_REGION = "us-west-2"
COGNITO_USER_POOL_ID = "us-west-2_skfkpmVv6"
COGNITO_CLIENT_ID = "3aiakr6qdoqtajv7qgtapecerg"
REQUEST_TIMEOUT_SECONDS = 20
CONNECT_ITEM_ID = os.getenv("APRILAIRE_CONNECT_ITEM_ID")
TYPES_PROCESSED = [CLIMATE_TYPE_APRILAIRE]
ZONE_BY_HIERARCHY = {1: "PZ1", 2: "SZ2", 3: "SZ3"}


def check_types(config_data):
    try:
        type_id = int(config_data.split("|")[0])
        if type_id and type_id in TYPES_PROCESSED:
            return True
        if type_id == 0:
            return True
        return False
    except (ValueError, IndexError, AttributeError):
        return False


def get_credentials():
    credentials = connect.get_credentials(os.getenv("APRILAIRE_CONNECT_ITEM_ID", CONNECT_ITEM_ID))
    if not credentials or len(credentials) < 2:
        raise ValueError("Missing AprilAire credentials")
    return credentials[0].value, credentials[1].value


def get_id_token(username, password):
    cognito = Cognito(
        user_pool_id=COGNITO_USER_POOL_ID,
        client_id=COGNITO_CLIENT_ID,
        user_pool_region=COGNITO_REGION,
        username=username,
    )
    cognito.authenticate(password=password)
    return cognito.id_token


def get_json(session, url, token_factory):
    for attempt in range(2):
        response = session.get(
            url,
            headers={
                "Accept": "application/json",
                "Authorization": "Bearer " + token_factory(),
                "Content-Type": "application/json",
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )

        if response.status_code == 401 and attempt == 0:
            token_factory(refresh=True)
            continue

        if response.status_code != 200:
            logging.error(f"Bad response from aprilaire {response.status_code}")
            raise Exception(f"Bad response from aprilaire {response.status_code}")

        if not response.content:
            return {}

        payload = json.loads(response.content.decode())
        if not isinstance(payload, dict):
            raise ValueError("Unexpected AprilAire response payload")
        return payload

    raise Exception("AprilAire authentication rejected the request")


def get_hierarchy_device_zones(session, token_factory):
    hierarchy = get_json(session, f"{DEVICE_URL}/hierarchy", token_factory)
    device_zones = {}

    for location in hierarchy.get("locations", []):
        if not isinstance(location, dict):
            continue
        for room in location.get("rooms", []):
            if not isinstance(room, dict):
                continue
            for device in room.get("devices", []):
                if not isinstance(device, dict):
                    continue
                device_id = device.get("deviceId")
                zone = device.get("zone")
                if isinstance(device_id, str):
                    device_zones[device_id] = ZONE_BY_HIERARCHY.get(zone, "PZ1")

    return device_zones


def get_device_settings(session, token_factory, device_id):
    return get_json(session, f"{DEVICE_URL}/{device_id}/settings", token_factory)


def get_status_payload(session, token_factory, device_id, status):
    return get_json(session, f"{DEVICE_URL}/{device_id}/status/{status}", token_factory)


def select_sensor_reading(sensors):
    if not isinstance(sensors, list):
        return None

    valid = []
    for sensor in sensors:
        if not isinstance(sensor, dict):
            continue
        try:
            reading = float(sensor["reading"])
        except (KeyError, TypeError, ValueError):
            continue
        valid.append((sensor, reading))

    for sensor, reading in valid:
        if sensor.get("isControlling") is True:
            return reading

    for sensor, reading in valid:
        if sensor.get("status") == "reporting" and sensor.get("isPrimary") is True:
            return reading

    return valid[0][1] if valid else None


def get_current_humidity(status_payload, fallback_status=None):
    current_humidity = select_sensor_reading(status_payload.get("humSensors"))
    if current_humidity is not None:
        return current_humidity

    try:
        return float(status_payload["currentHumidity"])
    except (KeyError, TypeError, ValueError):
        pass

    if isinstance(fallback_status, dict):
        current_humidity = select_sensor_reading(fallback_status.get("humSensors"))
        if current_humidity is not None:
            return current_humidity
        try:
            return float(fallback_status["currentHumidity"])
        except (KeyError, TypeError, ValueError):
            return 0.0

    return 0.0


def apply_dehumidifier(sensor, settings_payload, status_payload):
    settings = settings_payload.get("dehumidifier", {})
    if not isinstance(settings, dict):
        settings = {}
    alerts = status_payload.get("alerts", {})
    if not isinstance(alerts, dict):
        alerts = {}
    filter_service = status_payload.get("filterService", {})
    if not isinstance(filter_service, dict):
        filter_service = {}

    sensor.profile = "dehumidifier"
    sensor.mode = str(settings.get("mode", sensor.mode))
    sensor.state = str(status_payload.get("equipmentStatus", ""))
    sensor.humidity_set = float(settings.get("humiditySetpoint", 0.0) or 0.0)
    sensor.humidity = get_current_humidity(status_payload)
    sensor.isCompOn = bool(status_payload.get("isCompOn", False))
    sensor.isDehumFanOn = bool(status_payload.get("isDehumFanOn", False))
    sensor.isHvacFanOn = bool(status_payload.get("isHvacFanOn", False))
    sensor.alerts = alerts
    sensor.fanTimeHours = int(status_payload.get("fanTimeHours", 0) or 0)
    sensor.filterService = filter_service


def apply_humidifier(sensor, settings_payload, status_payload, thermostat_status=None):
    settings = settings_payload.get("humidifier", {})
    if not isinstance(settings, dict):
        settings = {}

    sensor.profile = "humidifier"
    sensor.mode = str(settings.get("mode", sensor.mode))
    sensor.state = str(status_payload.get("equipmentStatus", ""))
    sensor.humidity_set = float(settings.get("humiditySetpoint", 0.0) or 0.0)
    sensor.humidity = get_current_humidity(status_payload, thermostat_status)


def populate_sensor(session, token_factory, sensor, zone_key):
    settings_payload = get_device_settings(session, token_factory, sensor.key)

    if isinstance(settings_payload.get("dehumidifier"), dict):
        status_payload = get_status_payload(session, token_factory, sensor.key, "dehumidifier")
        apply_dehumidifier(sensor, settings_payload, status_payload)
        return True

    if isinstance(settings_payload.get("humidifier"), dict):
        status_payload = get_status_payload(session, token_factory, sensor.key, "humidifier")
        thermostat_status = None
        if zone_key:
            thermostat_status = get_status_payload(
                session,
                token_factory,
                sensor.key,
                f"thermostat/{zone_key}",
            )
        apply_humidifier(sensor, settings_payload, status_payload, thermostat_status)
        return True

    logging.error(f"Unsupported AprilAire settings profile for {sensor.key}")
    return False


def get_weather(home):
    session = requests.Session()
    try:
        sensors = []
        for key, value in os.environ.items():
            config_data = os.getenv(key)
            if key.startswith("CLIMATE_SENSOR") and check_types(config_data):
                sensors.append(home.climate.create_sensor(config_data))

        if len(sensors) == 0:
            return

        username, password = get_credentials()
        token_cache = {"id_token": None}

        def token_factory(refresh=False):
            if refresh or token_cache["id_token"] is None:
                token_cache["id_token"] = get_id_token(username, password)
            return token_cache["id_token"]

        get_json(session, ACCOUNT_URL, token_factory)
        device_zones = get_hierarchy_device_zones(session, token_factory)


        for sensor in sensors:
            try:
                if populate_sensor(session, token_factory, sensor, device_zones.get(sensor.key)):
                    home.climate.sensors.append(sensor)
            except Exception as e:
                traceback.print_exc()
                logging.error(f"Unable to get aprilaire:sensor {sensor.key} {e}")
                print(dt.datetime.now().time(), "Unable to get aprilaire:get_weather ")

    except Exception as e:
        traceback.print_exc()
        logging.error(f"Unable to get aprilaire:get_weather {e}")
        print(dt.datetime.now().time(), "Unable to get aprilaire:get_weather ")
    finally:
        session.close()
