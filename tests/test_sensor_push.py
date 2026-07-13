import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch, MagicMock
from stations import sensorPush
from weather import data


class TestSensorPush(unittest.TestCase):

    @patch('stations.sensorPush.requests.post')
    @patch('stations.sensorPush.connect.get_credentials')
    def test_get_authorization_success(self, mock_credentials, mock_post):
        """Test successful authorization."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = '{"authorization": "test_auth"}'
        mock_post.return_value = mock_response

        result = sensorPush.get_authorization()
        self.assertEqual(result, "test_auth")

    @patch('stations.sensorPush.requests.post')
    @patch('stations.sensorPush.connect.get_credentials')
    def test_get_authorization_failure(self, mock_credentials, mock_post):
        """Test authorization failure."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        result = sensorPush.get_authorization()
        self.assertIsNone(result)

    @patch('stations.sensorPush.get_authorization')
    @patch('stations.sensorPush.get_access_token')
    @patch('stations.sensorPush.get_sensor_data')
    def test_get_weather_no_data(self, mock_sensor_data, mock_access_token, mock_auth):
        """Test get_weather when no sensor data is available."""
        mock_auth.return_value = "auth"
        mock_access_token.return_value = "token"
        mock_sensor_data.return_value = None

        home = data.Home()
        sensorPush.get_weather(home)

        # Should not crash, and home object remains valid
        self.assertIsNotNone(home)

    @patch('stations.sensorPush.get_authorization')
    @patch('stations.sensorPush.get_access_token')
    @patch('stations.sensorPush.get_sensor_data')
    def test_get_weather_with_data(self, mock_sensor_data, mock_access_token, mock_auth):
        """Test get_weather with mock sensor data."""
        mock_auth.return_value = "auth"
        mock_access_token.return_value = "token"

        # Mock calibration data
        mock_sensor_data.side_effect = [
            {"sensors": {"test_key": {"calibration": {"temperature": 0, "humidity": 0}}}},
            {"sensors": {"16867526": [{"temperature": 70, "humidity": 50, "observed": "2023-01-01T12:00:00Z"}]}}
        ]

        home = data.Home()
        sensorPush.get_weather(home)

        # Ensure no exception and home object is valid
        self.assertIsNotNone(home)

    def test_check_types_valid(self):
        """Test check_types with valid type."""
        result = sensorPush.check_types("10|1|key|label")
        self.assertTrue(result)

    def test_check_types_zero(self):
        """Test check_types with type 0 (always valid)."""
        result = sensorPush.check_types("0|1|key|label")
        self.assertTrue(result)

    def test_check_types_invalid(self):
        """Test check_types with invalid type."""
        result = sensorPush.check_types("99|1|key|label")
        self.assertFalse(result)

    def test_check_types_invalid_format(self):
        """Test check_types with malformed config."""
        result = sensorPush.check_types("invalid")
        self.assertFalse(result)

    def test_get_sensor_by_key_found(self):
        """Test get_sensor_by_key when sensor is found."""
        sensors = [MagicMock(key="sensor1"), MagicMock(key="sensor2")]
        result = sensorPush.get_sensor_by_key(sensors, "sensor1_data")
        self.assertEqual(result, sensors[0])

    def test_get_sensor_by_key_not_found(self):
        """Test get_sensor_by_key when sensor is not found."""
        sensors = [MagicMock(key="sensor1"), MagicMock(key="sensor2")]
        result = sensorPush.get_sensor_by_key(sensors, "sensor3_data")
        self.assertIsNone(result)

    def test_get_sensor_by_key_empty_list(self):
        """Test get_sensor_by_key with empty sensor list."""
        result = sensorPush.get_sensor_by_key([], "sensor1_data")
        self.assertIsNone(result)

    @patch('stations.sensorPush.requests.post')
    def test_get_access_token_success(self, mock_post):
        """Test successful access token retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = '{"accesstoken": "test_access_token"}'
        mock_post.return_value = mock_response

        result = sensorPush.get_access_token("auth_header")
        self.assertEqual(result, "test_access_token")

    @patch('stations.sensorPush.requests.post')
    def test_get_access_token_failure(self, mock_post):
        """Test access token retrieval failure."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        result = sensorPush.get_access_token("auth_header")
        self.assertIsNone(result)

    @patch('stations.sensorPush.requests.post')
    def test_get_sensor_data_success(self, mock_post):
        """Test successful sensor data retrieval."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = '{"sensors": {"key1": [{"temperature": 70}]}}'
        mock_post.return_value = mock_response

        result = sensorPush.get_sensor_data("token", "http://test.com")
        self.assertEqual(result["sensors"]["key1"][0]["temperature"], 70)

    @patch('stations.sensorPush.requests.post')
    def test_get_sensor_data_failure(self, mock_post):
        """Test sensor data retrieval failure."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = sensorPush.get_sensor_data("token", "http://test.com")
        self.assertIsNone(result)

    @patch('stations.sensorPush.requests.post')
    def test_get_sensor_data_empty(self, mock_post):
        """Test sensor data retrieval with empty response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = '{}'
        mock_post.return_value = mock_response

        result = sensorPush.get_sensor_data("token", "http://test.com")
        self.assertIsNone(result)

    @patch('stations.sensorPush.connect.get_credentials')
    def test_get_authorization_exception(self, mock_credentials):
        """Test get_authorization with exception."""
        mock_credentials.side_effect = Exception("Connection error")
        result = sensorPush.get_authorization()
        self.assertIsNone(result)

    def test_apply_sensor_success(self):
        """Test applying sensor data with valid calibration."""
        mock_sensor = MagicMock()
        sensor_data = {
            "sensors": {
                "test_key": [
                    {"temperature": 70.5, "humidity": 50.0, "observed": "2023-01-01T12:00:00Z"},
                    {"temperature": 71.0, "humidity": 51.0, "observed": "2023-01-01T12:00:01Z"}
                ]
            }
        }
        calibration_data = {
            "test_key": {
                "calibration": {
                    "temperature": 1.5,
                    "humidity": -2.0
                }
            }
        }

        sensorPush.apply_sensor(mock_sensor, sensor_data, calibration_data, "test_key")

        self.assertIsNotNone(mock_sensor.temperature)
        self.assertIsNotNone(mock_sensor.humidity)
        self.assertIsNotNone(mock_sensor.time)

    def test_apply_sensor_missing_key(self):
        """Test apply_sensor with missing sensor key."""
        mock_sensor = MagicMock()
        sensor_data = {"sensors": {"other_key": []}}
        calibration_data = {}

        # Should not raise exception
        sensorPush.apply_sensor(mock_sensor, sensor_data, calibration_data, "test_key")

    @patch.dict('stations.sensorPush.os.environ', {'CLIMATE_SENSOR_1': '10|1|key|label'})
    @patch('stations.sensorPush.get_authorization')
    @patch('stations.sensorPush.get_access_token')
    @patch('stations.sensorPush.get_sensor_data')
    def test_get_weather_complete_flow(self, mock_sensor_data, mock_access_token, mock_auth):
        """Test complete get_weather flow with sensors."""
        mock_auth.return_value = "auth_token"
        mock_access_token.return_value = "access_token"

        calibration_data = {
            "16867526": {
                "calibration": {
                    "temperature": 0.5,
                    "humidity": -1.0
                }
            }
        }

        sensor_data = {
            "sensors": {
                "16867526": [
                    {"temperature": 70.0, "humidity": 50.0, "observed": "2023-01-01T12:00:00Z"}
                ]
            }
        }

        mock_sensor_data.side_effect = [calibration_data, sensor_data]

        home = data.Home()
        sensorPush.get_weather(home)

        self.assertIsNotNone(home)

    @patch.dict('stations.sensorPush.os.environ', {})
    @patch('stations.sensorPush.get_authorization')
    def test_get_weather_no_sensors_configured(self, mock_auth):
        """Test get_weather with no sensors configured."""
        mock_auth.return_value = "auth_token"
        home = data.Home()
        sensorPush.get_weather(home)

        self.assertIsNotNone(home)
        self.assertEqual(len(home.climate.sensors), 0)

    @patch.dict('stations.sensorPush.os.environ', {'CLIMATE_SENSOR_1': '10|1|key|label'})
    @patch('stations.sensorPush.get_authorization')
    def test_get_weather_no_auth(self, mock_auth):
        """Test get_weather when authorization fails."""
        mock_auth.return_value = None
        home = data.Home()
        sensorPush.get_weather(home)

        self.assertIsNotNone(home)
        self.assertEqual(len(home.climate.sensors), 0)

    @patch.dict('stations.sensorPush.os.environ', {
        'CLIMATE_SENSOR_1': '10|sensor1|label1',
        'CLIMATE_SENSOR_2': '10|sensor2|label2'
    })
    @patch('stations.sensorPush.get_authorization')
    @patch('stations.sensorPush.get_access_token')
    @patch('stations.sensorPush.get_sensor_data')
    @patch('stations.sensorPush.apply_sensor')
    def test_get_weather_continues_after_sensor_failure(self, mock_apply, mock_sensor_data, mock_access_token, mock_auth):
        """Test get_weather keeps processing later SensorPush sensors after one fails."""
        mock_auth.return_value = "auth_token"
        mock_access_token.return_value = "access_token"
        mock_sensor_data.side_effect = [
            {
                "sensors": {
                    "sensor1": {"calibration": {"temperature": 0.0, "humidity": 0.0}},
                    "sensor2": {"calibration": {"temperature": 0.0, "humidity": 0.0}}
                }
            },
            {
                "sensors": {
                    "sensor1": [{"temperature": 70.0, "humidity": 50.0, "observed": "2023-01-01T12:00:00Z"}],
                    "sensor2": [{"temperature": 71.0, "humidity": 51.0, "observed": "2023-01-01T12:00:00Z"}]
                }
            }
        ]
        mock_apply.side_effect = [Exception("bad sensor"), None]

        home = data.Home()
        sensorPush.get_weather(home)

        self.assertEqual(mock_apply.call_count, 2)
        self.assertEqual(len(home.climate.sensors), 1)
        self.assertEqual(home.climate.sensors[0].label, 'label2')


if __name__ == '__main__':
    unittest.main()
