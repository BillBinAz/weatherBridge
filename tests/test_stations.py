import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch, MagicMock
from weather import stations, data


class TestStations(unittest.TestCase):
    def test_calculate_humidity_average_uses_configured_labels(self):
        home = data.Home()
        sensor_a = data.SensorSmall("10|a|Kitchen")
        sensor_b = data.SensorSmall("10|b|Office")
        sensor_a.humidity = 41
        sensor_b.humidity = 55
        home.climate.sensors.extend([sensor_a, sensor_b])

        with patch.dict(os.environ, {"AVERAGE_HUMIDITY_KEYS": " Kitchen |Office|Missing "}):
            result = stations.calculate_humidity_average(home)

        self.assertIsNone(result)
        self.assertEqual(home.climate.home_average_humidity, 48.0)

    def test_calculate_humidity_average_skips_missing_and_none_values(self):
        home = data.Home()
        sensor = data.SensorSmall("10|a|Kitchen")
        sensor.humidity = None
        home.climate.sensors.append(sensor)

        with patch.dict(os.environ, {"AVERAGE_HUMIDITY_KEYS": "Kitchen|Missing"}):
            result = stations.calculate_humidity_average(home)

        self.assertIsNone(result)
        self.assertEqual(home.climate.home_average_humidity, 0.0)

    @patch('weather.stations.logging.error')
    def test_calculate_humidity_average_handles_invalid_humidity_type(self, mock_log_error):
        home = data.Home()
        sensor = data.SensorSmall("10|a|Kitchen")
        sensor.humidity = "bad-value"
        home.climate.sensors.append(sensor)

        with patch.dict(os.environ, {"AVERAGE_HUMIDITY_KEYS": "Kitchen"}):
            result = stations.calculate_humidity_average(home)

        self.assertIsNone(result)
        self.assertEqual(home.climate.home_average_humidity, 0.0)
        mock_log_error.assert_called_once()

    @patch('weather.stations.home_assistant.get_weather')
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_calls_all_stations(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that get_weather calls all station modules."""
        home = stations.get_weather()

        self.assertIsInstance(home, data.Home)
        mock_home.assert_called_once()
        mock_wifi.assert_called_once()
        mock_sensor.assert_called_once()
        mock_thermo.assert_called_once()

    @patch('weather.stations.home_assistant.get_weather')
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_calculates_average_temp(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that Home object is created correctly."""
        mock_home.return_value = None
        mock_wifi.return_value = None
        mock_sensor.return_value = None
        mock_thermo.return_value = None

        result = stations.get_weather()

        # Verify result is a Home object
        self.assertIsInstance(result, data.Home)
        self.assertIsInstance(result.alarm, data.Alarm)
        self.assertIsInstance(result.climate, data.Climate)

    @patch('weather.stations.home_assistant.get_weather')
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_handles_exception(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that get_weather keeps collecting after home_assistant fails."""
        mock_home.side_effect = Exception("Connection error")
        mock_wifi.return_value = None
        mock_sensor.return_value = None
        mock_thermo.return_value = None

        result = stations.get_weather()

        self.assertIsInstance(result, data.Home)
        mock_home.assert_called_once()
        mock_wifi.assert_called_once()
        mock_sensor.assert_called_once()
        mock_thermo.assert_called_once()

    @patch('weather.stations.home_assistant.get_weather')
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_exception_in_wifi_logger(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that get_weather keeps collecting after wifiLogger fails."""
        mock_home.return_value = None
        mock_wifi.side_effect = RuntimeError("WiFi error")
        mock_sensor.return_value = None
        mock_thermo.return_value = None

        result = stations.get_weather()

        self.assertIsInstance(result, data.Home)
        mock_home.assert_called_once()
        mock_wifi.assert_called_once()
        mock_sensor.assert_called_once()
        mock_thermo.assert_called_once()

    @patch('weather.stations.home_assistant.get_weather')
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_exception_in_thermo_works(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that get_weather keeps collecting after thermo_works fails."""
        mock_home.return_value = None
        mock_wifi.return_value = None
        mock_sensor.return_value = None
        mock_thermo.side_effect = ValueError("Device not found")

        result = stations.get_weather()

        self.assertIsInstance(result, data.Home)
        mock_home.assert_called_once()
        mock_wifi.assert_called_once()
        mock_sensor.assert_called_once()
        mock_thermo.assert_called_once()

if __name__ == '__main__':
    unittest.main()
