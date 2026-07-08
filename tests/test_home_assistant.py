import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch, MagicMock
from stations import home_assistant
from weather import data


class TestHomeAssistant(unittest.TestCase):

    @patch('stations.home_assistant.connect.get_credentials')
    def test_get_bearer_token_success(self, mock_credentials):
        """Test successful bearer token retrieval."""
        mock_credentials.return_value = [MagicMock(value="test_token")]
        result = home_assistant.get_bearer_token()
        self.assertEqual(result, "test_token")

    @patch('stations.home_assistant.connect.get_credentials')
    def test_get_bearer_token_failure(self, mock_credentials):
        """Test bearer token retrieval failure."""
        mock_credentials.side_effect = Exception("Connection error")
        result = home_assistant.get_bearer_token()
        self.assertIsNone(result)

    @patch.dict('stations.home_assistant.os.environ', {'HOME_ASSISTANT_URL': 'http://test.com/'})
    @patch('stations.home_assistant.HOME_ASSISTANT_URL', 'http://test.com/')
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    def test_get_sensor_data_success(self, mock_token, mock_session):
        """Test successful sensor data retrieval."""
        mock_token.return_value = "token"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = '{"state": "75.0"}'
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        result = home_assistant.get_sensor_data("token", "test_entity", mock_session_instance)
        self.assertEqual(result["state"], "75.0")

    @patch('stations.home_assistant.HOME_ASSISTANT_URL', 'http://test.com/')
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    def test_get_sensor_data_failure(self, mock_token, mock_session):
        """Test sensor data retrieval failure."""
        mock_token.return_value = "token"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        result = home_assistant.get_sensor_data("token", "test_entity", mock_session_instance)
        self.assertIsNone(result)

    def test_get_temperature(self):
        """Test temperature extraction from sensor data."""
        sensor_data = {"state": "72.5"}
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = sensor_data
            result = home_assistant.get_value("token", "entity", MagicMock())
            self.assertEqual(result, 72.5)

    def test_get_occupancy_on(self):
        """Test occupancy when sensor is on."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "on"}
            result = home_assistant.get_occupancy("token", "entity", MagicMock())
            self.assertEqual(result, 1)

    def test_get_occupancy_off(self):
        """Test occupancy when sensor is off."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "off"}
            result = home_assistant.get_occupancy("token", "entity", MagicMock())
            self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
