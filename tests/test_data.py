import unittest
import json
from weather import data


class TestData(unittest.TestCase):

    def test_weather_data_creation(self):
        """Test that WeatherData initializes all attributes correctly."""
        weather = data.WeatherData()

        # Check main weather station
        self.assertIsInstance(weather.back_yard, data.SensorMajor)
        self.assertEqual(weather.back_yard.temp, 'None')

        # Check alarm
        self.assertIsInstance(weather.alarm, data.Alarm)
        self.assertEqual(weather.alarm.status, 0)

        # Check sensor push
        self.assertIsInstance(weather.rack, data.SensorSmallWithCalibration)
        self.assertEqual(weather.rack.temp, 'None')

        # Check ecobee sensors
        self.assertIsInstance(weather.hallway_thermostat, data.SensorThermostat)
        self.assertIsInstance(weather.bedroom_left, data.EcobeeSensor)

        # Check node sensors
        self.assertIsInstance(weather.humidor, data.NodeTempHumidity)
        self.assertIsInstance(weather.garage, data.NodeTemp)

        # Check whole house fan
        self.assertIsInstance(weather.whole_house_fan, data.WholeHomeFan)
        self.assertEqual(weather.whole_house_fan.speed, "")

    def test_to_json(self):
        """Test that to_json produces valid JSON."""
        weather = data.WeatherData()
        weather.back_yard.temp = "75.0"
        weather.alarm.status = 1

        json_str = weather.to_json()
        parsed = json.loads(json_str)

        self.assertIn('back_yard', parsed)
        self.assertEqual(parsed['back_yard']['temp'], '75.0')
        self.assertEqual(parsed['alarm']['status'], 1)

    def test_weather_data_to_json(self):
        """Test to_json with nested objects."""
        weather = data.WeatherData()
        weather.back_yard.temp = "75.0"
        weather.alarm.status = 1
        weather.hallway_thermostat.mode = "Heat"

        json_str = weather.to_json()
        parsed = json.loads(json_str)

        self.assertEqual(parsed['back_yard']['temp'], '75.0')
        self.assertEqual(parsed['alarm']['status'], 1)
        self.assertEqual(parsed['hallway_thermostat']['mode'], 'Heat')

    def test_sensor_classes(self):
        """Test individual sensor class initializations."""
        sensor = data.SensorSmall()
        self.assertEqual(sensor.temp, 'None')
        self.assertEqual(sensor.temp_c, 'None')
        self.assertEqual(sensor.humidity, 0.0)

        sensor_cal = data.SensorSmallWithCalibration()
        self.assertEqual(sensor_cal.temp_calibration, 0.0)
        self.assertEqual(sensor_cal.humidity_calibration, 0.0)

        sensor_major = data.SensorMajor()
        self.assertEqual(sensor_major.wind_direction, "")
        self.assertEqual(sensor_major.pressure, 0)

        thermostat = data.SensorThermostat()
        self.assertIsInstance(thermostat.sensor, data.EcobeeSensor)

        ecobee = data.EcobeeSensor()
        self.assertEqual(ecobee.temp, 'None')
        self.assertEqual(ecobee.occupied, 0)

    def test_alarm_initialization(self):
        """Test Alarm class initialization."""
        alarm = data.Alarm()
        self.assertEqual(alarm.status, 0)
        self.assertEqual(alarm.status_label, "None")
        self.assertEqual(alarm.all_zones_closed, 0)

    def test_thermostat_initialization(self):
        """Test SensorThermostat initialization."""
        thermo = data.SensorThermostat()
        self.assertEqual(thermo.temp, 'None')
        self.assertEqual(thermo.mode, "")
        self.assertIsInstance(thermo.sensor, data.EcobeeSensor)

    def test_whole_home_fan_initialization(self):
        """Test WholeHomeFan initialization."""
        fan = data.WholeHomeFan()
        self.assertEqual(fan.speed, "")
        self.assertEqual(fan.houseTemp, "")
        self.assertEqual(fan.fan_zones_all, 0)


if __name__ == '__main__':
    unittest.main()
