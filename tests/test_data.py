import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import json
from weather import data


class TestData(unittest.TestCase):

    def test_weather_data_creation(self):
        """Test that Home initializes all attributes correctly."""
        home = data.Home()

        # Check alarm
        self.assertIsInstance(home.alarm, data.Alarm)
        self.assertEqual(home.alarm.all_zones_closed, 1)
        self.assertEqual(home.alarm.status_value, 0)

        # Check climate
        self.assertIsInstance(home.climate, data.Climate)
        self.assertEqual(home.climate.home_average_temperature, 0.0)
        self.assertEqual(home.climate.home_average_humidity, 0.0)

        # Check doors
        self.assertIsInstance(home.doors, list)

    def test_to_json(self):
        """Test that to_json produces valid JSON."""
        home = data.Home()
        home.alarm.status_value = 1
        home.alarm.status_label = "Armed"

        json_str = home.to_json()
        parsed = json.loads(json_str)

        self.assertIn('alarm', parsed)
        self.assertEqual(parsed['alarm']['status_value'], 1)
        self.assertEqual(parsed['alarm']['status_label'], 'Armed')

    def test_weather_data_to_json(self):
        """Test to_json with nested objects."""
        home = data.Home()
        home.alarm.status_value = 1
        home.climate.home_average_temperature = 72.5
        home.climate.home_average_humidity = 51.0

        json_str = home.to_json()
        parsed = json.loads(json_str)

        self.assertEqual(parsed['alarm']['status_value'], 1)
        self.assertEqual(parsed['climate']['home_average_temperature'], 72.5)
        self.assertEqual(parsed['climate']['home_average_humidity'], 51.0)

    def test_sensor_classes(self):
        """Test individual sensor class initializations."""
        sensor = data.SensorSmall("10|test_key|Test Label")
        self.assertEqual(sensor.temperature, 'None')
        self.assertEqual(sensor.temperature_c, 'None')
        self.assertEqual(sensor.humidity, 0.0)

        sensor_push = data.SensorPush("10|test_key|Test Label")
        self.assertEqual(sensor_push.temperature_calibration, 0.0)
        self.assertEqual(sensor_push.humidity_calibration, 0.0)

        sensor_aprilaire = data.SensorAprilaire("13|device_id|AprilAire")
        self.assertEqual(sensor_aprilaire.profile, "")
        self.assertEqual(sensor_aprilaire.mode, "off")
        self.assertFalse(sensor_aprilaire.is_comp_on)
        self.assertFalse(sensor_aprilaire.is_dehum_fan_on)
        self.assertFalse(sensor_aprilaire.is_hvac_fan_on)
        self.assertEqual(sensor_aprilaire.alerts, {})
        self.assertEqual(sensor_aprilaire.fan_time_hours, 0)
        self.assertEqual(sensor_aprilaire.filter_service, {})

        sensor_davis = data.SensorDavisWeatherStation("4|Test Station|http://test.com")
        self.assertEqual(sensor_davis.wind_direction, "")
        self.assertEqual(sensor_davis.pressure, 0)

        ecobee = data.SensorEcobee("6|test_key|Test Ecobee")
        self.assertEqual(ecobee.temperature, 'None')
        self.assertEqual(ecobee.occupied, 0)

    def test_alarm_initialization(self):
        """Test Alarm class initialization."""
        alarm = data.Alarm()
        self.assertEqual(alarm.status_value, 0)
        self.assertEqual(alarm.status_label, "None")
        self.assertEqual(alarm.all_zones_closed, 1)
        self.assertIsInstance(alarm.zones, list)

    def test_thermostat_initialization(self):
        """Test SensorEcobeeThermostat initialization."""
        thermo = data.SensorEcobeeThermostat("5|test_key|Test Thermostat")
        self.assertEqual(thermo.temperature, 'None')
        self.assertEqual(thermo.mode, "")
        self.assertEqual(thermo.heat_set, 0.0)
        self.assertEqual(thermo.cool_set, 0.0)

    def test_whole_home_fan_initialization(self):
        """Test Climate initialization (home average temperature)."""
        climate = data.Climate()
        self.assertEqual(climate.home_average_temperature, 0.0)
        self.assertEqual(climate.home_average_humidity, 0.0)
        self.assertIsInstance(climate.sensors, list)

    def test_create_sensor_davis(self):
        """Test Climate.create_sensor with Davis type."""
        climate = data.Climate()
        config = "4|Davis|Test Station|http://test.com"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorDavisWeatherStation)

    def test_create_sensor_ecobee_thermostat(self):
        """Test Climate.create_sensor with Ecobee Thermostat type."""
        climate = data.Climate()
        config = "5|ecobee|Main Thermostat"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorEcobeeThermostat)

    def test_create_sensor_ecobee_sensor(self):
        """Test Climate.create_sensor with Ecobee Sensor type."""
        climate = data.Climate()
        config = "6|ecobee_sensor|Master Bedroom"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorEcobee)

    def test_create_sensor_thermoworks_node(self):
        """Test Climate.create_sensor with ThermoWorks Node type."""
        climate = data.Climate()
        config = "7|thermoworks|Freezer"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorThermoworksNode)

    def test_create_sensor_thermoworks_humidity(self):
        """Test Climate.create_sensor with ThermoWorks Humidity type."""
        climate = data.Climate()
        config = "8|thermoworks_humid|Office"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorThermoworksNodeWithHumidity)

    def test_create_sensor_thermoworks_two_channel(self):
        """Test Climate.create_sensor with ThermoWorks Two Channel type."""
        climate = data.Climate()
        config = "9|thermoworks_2ch|Fridge"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorThermoworksNodeTwoProbes)

    def test_create_sensor_sensor_push(self):
        """Test Climate.create_sensor with SensorPush type."""
        climate = data.Climate()
        config = "10|sensor_push|Outside"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorPush)

    def test_create_sensor_humidity(self):
        """Test Climate.create_sensor with Humidity type."""
        climate = data.Climate()
        config = "11|humidifier|Living Room"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorHumidifier)

    def test_create_sensor_aprilaire(self):
        """Test Climate.create_sensor with AprilAire type."""
        climate = data.Climate()
        config = "13|device_id|Basement AprilAire"
        sensor = climate.create_sensor(config)
        self.assertIsInstance(sensor, data.SensorAprilaire)

    def test_create_sensor_invalid_type(self):
        """Test Climate.create_sensor with invalid type."""
        climate = data.Climate()
        config = "999|invalid|Invalid"
        with self.assertRaises(ValueError) as context:
            climate.create_sensor(config)
        self.assertIn("Unknown sensor type", str(context.exception))

    def test_climate_to_json(self):
        """Test Climate.to_json with sensors."""
        climate = data.Climate()
        sensor = data.SensorSmall("10|test_key|Test Sensor")
        sensor.temperature = 75.0
        climate.sensors.append(sensor)
        
        json_str = climate.to_json()
        parsed = json.loads(json_str)
        self.assertIn('Test Sensor', parsed)

    def test_door_initialization(self):
        """Test Door class initialization."""
        door = data.Door()
        self.assertEqual(door.label, "None")
        self.assertEqual(door.locked, 0)

    def test_alarm_zone_initialization(self):
        """Test AlarmZone class initialization."""
        config = "1|1|zone1|Front Door"
        zone = data.AlarmZone(config)
        self.assertEqual(zone.type, 1)
        self.assertEqual(zone.id, 1)


if __name__ == '__main__':
    unittest.main()
