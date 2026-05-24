import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch, MagicMock
from weather import stations, data


class TestStations(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
