import unittest
import json
from unittest.mock import patch
from get_handler import app


class TestGetHandler(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('get_handler.stations.get_weather')
    def test_get_weather_route(self, mock_get_weather):
        """Test the /weather GET route."""
        # Mock the weather data
        mock_weather_data = unittest.mock.MagicMock()
        mock_weather_data.to_json.return_value = '{"test": "data"}'
        mock_get_weather.return_value = mock_weather_data

        response = self.app.get('/weather')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json; charset=utf-8')
        self.assertEqual(response.get_data(as_text=True), '{"test": "data"}')
        mock_get_weather.assert_called_once()

    @patch('get_handler.stations.get_weather')
    def test_get_weather_route_json_response(self, mock_get_weather):
        """Test that the response is valid JSON."""
        mock_weather_data = unittest.mock.MagicMock()
        mock_weather_data.to_json.return_value = '{"temperature": 75, "humidity": 50}'
        mock_get_weather.return_value = mock_weather_data

        response = self.app.get('/weather')

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['temperature'], 75)
        self.assertEqual(data['humidity'], 50)

    def test_invalid_route(self):
        """Test accessing an invalid route."""
        response = self.app.get('/invalid')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
