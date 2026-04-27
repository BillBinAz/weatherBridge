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

        result = wifiLogger.get_data()
        self.assertEqual(result["tempout"], 75.5)
        self.assertEqual(result["humout"], 60)

    @patch('stations.wifiLogger.requests.get')
    def test_get_data_failure(self, mock_get):
        """Test data retrieval failure."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = wifiLogger.get_data()
        self.assertIsNone(result)

    def test_convert_to_float_valid(self):
        """Test convert_to_float with valid input."""
        result = wifiLogger.convert_to_float("75.5", 2)
        self.assertEqual(result, 75.5)

    def test_convert_to_float_invalid(self):
        """Test convert_to_float with invalid input."""
        result = wifiLogger.convert_to_float("invalid", 2)
        self.assertEqual(result, 0.0)

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

        weather_data = data.WeatherData()
        wifiLogger.get_weather(weather_data)

        self.assertEqual(weather_data.back_yard.temp, 75.5)
        self.assertEqual(weather_data.back_yard.humidity, 60.0)
        self.assertEqual(weather_data.back_yard.wind_direction, " S ")
        self.assertEqual(weather_data.back_yard.pressure, 29.92)

    @patch('stations.wifiLogger.get_data')
    def test_get_weather_no_data(self, mock_get_data):
        """Test get_weather when no data is available."""
        mock_get_data.return_value = None

        weather_data = data.WeatherData()
        wifiLogger.get_weather(weather_data)

        # Data should remain default
        self.assertEqual(weather_data.back_yard.temp, 'None')

    @patch('stations.wifiLogger.get_data')
    def test_get_weather_json_error(self, mock_get_data):
        """Test get_weather with JSON parsing error."""
        mock_get_data.side_effect = json.JSONDecodeError("Test error", "", 0)

        weather_data = data.WeatherData()
        wifiLogger.get_weather(weather_data)

        # Should not crash
        self.assertEqual(weather_data.back_yard.temp, 'None')


if __name__ == '__main__':
    unittest.main()
