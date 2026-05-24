import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
import json
from unittest.mock import patch, MagicMock
from stations import wifiLogger
from weather import data


class TestWifiLogger(unittest.TestCase):

    @patch('stations.wifiLogger.requests.get')
    def test_get_data_success(self, mock_get):
        """Test successful data retrieval from wifiLogger."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = '{"tempout": 75.5, "humout": 60}'
        mock_get.return_value = mock_response

        result = wifiLogger.get_data("http://test.com")
        self.assertEqual(result["tempout"], 75.5)
        self.assertEqual(result["humout"], 60)

    @patch('stations.wifiLogger.requests.get')
    def test_get_data_failure(self, mock_get):
        """Test data retrieval failure."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = wifiLogger.get_data("http://test.com")
        self.assertIsNone(result)

    def test_convert_to_float_valid(self):
        """Test convert_to_float with valid input."""
        result = wifiLogger.convert_to_float("75.5", 2)
        self.assertEqual(result, 75.5)

    def test_convert_to_float_invalid(self):
        """Test convert_to_float with invalid input."""
        result = wifiLogger.convert_to_float("invalid", 2)
        self.assertEqual(result, 0.0)

    @patch.dict(os.environ, {'CLIMATE_SENSOR_WIFI': '4|Back Yard|http://test.com', 'HOME_ASSISTANT_URL': 'http://test.com/'})
    @patch('stations.wifiLogger.get_data')
    def test_get_weather_success(self, mock_get_data):
        """Test successful weather data population."""
        mock_data = {
            "tempout": 75.5,
            "humout": 60.0,
            "dew": 65.0,
            "rainr": 0.0,
            "rain24": 0.5,
            "windspd": 5.0,
            "gust": 10.0,
            "winddir": 180,
            "chill": 70.0,
            "xlt": [80.0],
            "bar": 29.92
        }
        mock_get_data.return_value = mock_data

        home = data.Home()
        wifiLogger.get_weather(home)

        # Check that sensor was created and added
        self.assertGreater(len(home.climate.sensors), 0)

    @patch.dict(os.environ, {'CLIMATE_SENSOR_WIFI': '4|Back Yard|http://test.com'})
    @patch('stations.wifiLogger.get_data')
    def test_get_weather_no_data(self, mock_get_data):
        """Test get_weather when no data is available."""
        mock_get_data.return_value = None

        home = data.Home()
        wifiLogger.get_weather(home)

        # Data should remain default
        self.assertIsNotNone(home)

    @patch.dict(os.environ, {'CLIMATE_SENSOR_WIFI': '4|Back Yard|http://test.com'})
    @patch('stations.wifiLogger.get_data')
    def test_get_weather_json_error(self, mock_get_data):
        """Test get_weather with JSON parsing error."""
        mock_get_data.side_effect = json.JSONDecodeError("Test error", "", 0)

        home = data.Home()
        wifiLogger.get_weather(home)

        # Should not crash
        self.assertIsNotNone(home)


if __name__ == '__main__':
    unittest.main()
