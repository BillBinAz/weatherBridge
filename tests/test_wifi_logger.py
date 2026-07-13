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

    @patch('stations.wifiLogger.requests.get')
    def test_get_data_exception(self, mock_get):
        """Test get_data when an exception is raised."""
        mock_get.side_effect = Exception("Connection error")

        result = wifiLogger.get_data("http://test.com")
        self.assertIsNone(result)

    @patch('stations.wifiLogger.requests.get')
    def test_get_data_json_decode_error(self, mock_get):
        """Test get_data with invalid JSON response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = 'invalid json'
        mock_get.return_value = mock_response

        result = wifiLogger.get_data("http://test.com")
        self.assertIsNone(result)

    def test_check_types_valid(self):
        """Test check_types with valid config."""
        result = wifiLogger.check_types("4|test|url")
        self.assertTrue(result)

    def test_check_types_invalid_type(self):
        """Test check_types with invalid type."""
        result = wifiLogger.check_types("5|test|url")
        self.assertFalse(result)

    def test_check_types_invalid_format(self):
        """Test check_types with malformed config."""
        result = wifiLogger.check_types("invalid")
        self.assertFalse(result)

    def test_check_types_empty_config(self):
        """Test check_types with empty config."""
        result = wifiLogger.check_types("")
        self.assertFalse(result)

    @patch.dict(os.environ, {})
    def test_get_weather_no_config(self):
        """Test get_weather when no CLIMATE_SENSOR config exists."""
        home = data.Home()
        wifiLogger.get_weather(home)

        # Should return early without processing
        self.assertEqual(len(home.climate.sensors), 0)

    @patch.dict(os.environ, {'CLIMATE_SENSOR_WIFI': '4|Back Yard|http://test.com'})
    @patch('stations.wifiLogger.get_data')
    def test_get_weather_missing_key(self, mock_get_data):
        """Test get_weather when expected key is missing from data."""
        mock_data = {
            "tempout": 75.5
            # Missing other required keys
        }
        mock_get_data.return_value = mock_data

        home = data.Home()
        wifiLogger.get_weather(home)

        # Should handle KeyError gracefully
        self.assertIsNotNone(home)

    @patch.dict(os.environ, {'CLIMATE_SENSOR_WIFI': '4|Back Yard|http://test.com'})
    @patch('stations.wifiLogger.get_data')
    def test_get_weather_invalid_json_in_response(self, mock_get_data):
        """Test get_weather with invalid data structure."""
        mock_get_data.return_value = "not a dict"

        home = data.Home()
        wifiLogger.get_weather(home)

        # Should handle TypeError gracefully
        self.assertIsNotNone(home)

    @patch.dict(os.environ, {'CLIMATE_SENSOR_WIFI': '4|Back Yard|http://test.com'})
    @patch('stations.wifiLogger.get_data')
    def test_get_weather_general_exception(self, mock_get_data):
        """Test get_weather with general exception."""
        mock_get_data.side_effect = Exception("Unexpected error")

        home = data.Home()
        wifiLogger.get_weather(home)

        # Should handle exception gracefully
        self.assertIsNotNone(home)

    @patch.dict(os.environ, {
        'CLIMATE_SENSOR_WIFI_1': '4|Back Yard|http://test-one.com',
        'CLIMATE_SENSOR_WIFI_2': '4|Front Yard|http://test-two.com'
    })
    @patch('stations.wifiLogger.get_data')
    def test_get_weather_continues_after_sensor_failure(self, mock_get_data):
        """Test get_weather keeps processing later wifiLogger sensors after one fails."""
        mock_get_data.side_effect = [
            {'tempout': 75.5},
            {
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
        ]

        home = data.Home()
        wifiLogger.get_weather(home)

        self.assertEqual(len(home.climate.sensors), 1)
        self.assertEqual(home.climate.sensors[0].label, 'Front Yard')

    def test_convert_to_float_zero_precision(self):
        """Test convert_to_float with zero precision."""
        result = wifiLogger.convert_to_float("75.999", 0)
        self.assertEqual(result, 76.0)

    def test_convert_to_float_negative(self):
        """Test convert_to_float with negative value."""
        result = wifiLogger.convert_to_float("-10.5", 1)
        self.assertEqual(result, -10.5)

if __name__ == '__main__':
    unittest.main()
