import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

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

    @patch('get_handler.stations.get_weather')
    def test_get_weather_exception(self, mock_get_weather):
        """Test /weather endpoint when get_weather raises an exception."""
        mock_get_weather.side_effect = Exception("Database error")

        response = self.app.get('/weather')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Failed to retrieve weather data')

    def test_health_check_endpoint(self):
        """Test the /health GET route."""
        response = self.app.get('/health')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['status'], 'healthy')

    def test_health_check_json_response(self):
        """Test that /health returns valid JSON."""
        response = self.app.get('/health')

        self.assertEqual(response.content_type, 'application/json')
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, dict)
        self.assertIn('status', data)

    def test_404_error_handler(self):
        """Test 404 error handler."""
        response = self.app.get('/nonexistent/path')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['error'], 'Endpoint not found')

    @patch('get_handler.logger')
    def test_500_error_handler_logging(self, mock_logger):
        """Test that 500 error handler logs the error."""
        with patch('get_handler.stations.get_weather', side_effect=Exception("Test error")):
            response = self.app.get('/weather')

        self.assertEqual(response.status_code, 500)
        # Verify logging was called
        self.assertTrue(mock_logger.exception.called)

    def test_weather_endpoint_post_not_allowed(self):
        """Test that POST requests to /weather are not allowed."""
        response = self.app.post('/weather')
        self.assertEqual(response.status_code, 405)

    def test_health_endpoint_post_not_allowed(self):
        """Test that POST requests to /health are not allowed."""
        response = self.app.post('/health')
        self.assertEqual(response.status_code, 405)


if __name__ == '__main__':
    unittest.main()
