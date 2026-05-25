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
        self.assertEqual(home.alarm.all_zones_closed, 0)
        self.assertEqual(home.alarm.status_value, 0)

        # Check climate
        self.assertIsInstance(home.climate, data.Climate)
        self.assertEqual(home.climate.home_average_temperature, 0.0)

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

        json_str = home.to_json()
        parsed = json.loads(json_str)

        self.assertEqual(parsed['alarm']['status_value'], 1)
        self.assertEqual(parsed['climate']['home_average_temperature'], 72.5)

    def test_sensor_classes(self):
        """Test individual sensor class initializations."""
        sensor = data.SensorSmall("10|test_key|Test Label")
        self.assertEqual(sensor.temperature, 'None')
        self.assertEqual(sensor.temperature_c, 'None')
        self.assertEqual(sensor.humidity, 0.0)

        sensor_push = data.SensorPush("10|test_key|Test Label")
        self.assertEqual(sensor_push.temperature_calibration, 0.0)
        self.assertEqual(sensor_push.humidity_calibration, 0.0)

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
        self.assertEqual(alarm.all_zones_closed, 0)
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
        self.assertIsInstance(climate.sensors, list)


if __name__ == '__main__':
    unittest.main()
