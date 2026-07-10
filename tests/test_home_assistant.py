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

    def test_get_value_none(self):
        """Test get_value when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_value("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_occupancy_none(self):
        """Test get_occupancy when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_occupancy("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_garage_door_open(self):
        """Test garage door state when off (closed)."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "off"}
            result = home_assistant.get_garage_door("token", "entity", MagicMock())
            self.assertEqual(result, 1)

    def test_get_garage_door_closed(self):
        """Test garage door state when on (open)."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "on"}
            result = home_assistant.get_garage_door("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_garage_door_none(self):
        """Test garage door when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_garage_door("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_on_off_state_off(self):
        """Test on/off state when state is 'off'."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "off"}
            result = home_assistant.get_on_off_state("token", "entity", MagicMock())
            self.assertEqual(result, 1)

    def test_get_on_off_state_safe(self):
        """Test on/off state when state is 'Safe'."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "Safe"}
            result = home_assistant.get_on_off_state("token", "entity", MagicMock())
            self.assertEqual(result, 1)

    def test_get_on_off_state_on(self):
        """Test on/off state when state is 'on'."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "on"}
            result = home_assistant.get_on_off_state("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_on_off_state_none(self):
        """Test on/off state when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_on_off_state("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_locked_state_locked(self):
        """Test locked state when door is locked."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "locked"}
            result = home_assistant.get_locked_state("token", "entity", MagicMock())
            self.assertEqual(result, 1)

    def test_get_locked_state_unlocked(self):
        """Test locked state when door is unlocked."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "unlocked"}
            result = home_assistant.get_locked_state("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_locked_state_none(self):
        """Test locked state when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_locked_state("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_alarm_label_with_fault(self):
        """Test alarm label extraction with 'fault' in state."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "System Fault"}
            result = home_assistant.get_alarm_label("token", "entity", MagicMock())
            self.assertEqual(result, "Not Ready")

    def test_get_alarm_label_normal(self):
        """Test alarm label extraction with normal state."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "Ready"}
            result = home_assistant.get_alarm_label("token", "entity", MagicMock())
            self.assertEqual(result, "Ready")

    def test_get_alarm_label_with_asterisk(self):
        """Test alarm label extraction with asterisks."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "*Ready*"}
            result = home_assistant.get_alarm_label("token", "entity", MagicMock())
            self.assertEqual(result, "Ready")

    def test_get_alarm_label_truncation(self):
        """Test alarm label truncation to 10 characters."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "very_long_label"}
            result = home_assistant.get_alarm_label("token", "entity", MagicMock())
            self.assertEqual(result, "Very_Long_")

    def test_get_alarm_label_none(self):
        """Test alarm label when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_alarm_label("token", "entity", MagicMock())
            self.assertEqual(result, "")

    def test_get_alarm_status_armed(self):
        """Test alarm status when armed."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "armed_home"}
            result = home_assistant.get_alarm_status("token", "entity", MagicMock())
            self.assertEqual(result, 1)

    def test_get_alarm_status_disarmed(self):
        """Test alarm status when disarmed."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = {"state": "disarmed"}
            result = home_assistant.get_alarm_status("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_get_alarm_status_none(self):
        """Test alarm status when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_alarm_status("token", "entity", MagicMock())
            self.assertEqual(result, 0)

    def test_check_types_valid_type(self):
        """Test check_types with valid type."""
        result = home_assistant.check_types("5|1|entity|label")
        self.assertTrue(result)

    def test_check_types_invalid_type(self):
        """Test check_types with invalid type."""
        result = home_assistant.check_types("99|1|entity|label")
        self.assertFalse(result)

    def test_check_types_zero_type(self):
        """Test check_types with type 0 (always valid)."""
        result = home_assistant.check_types("0|1|entity|label")
        self.assertTrue(result)

    def test_check_types_invalid_format(self):
        """Test check_types with invalid format."""
        result = home_assistant.check_types("invalid")
        self.assertFalse(result)

    def test_check_types_missing_type(self):
        """Test check_types with empty string."""
        result = home_assistant.check_types("")
        self.assertFalse(result)

    def test_populate_ecobee_sensor(self):
        """Test populating ecobee sensor with temperature and occupancy."""
        mock_sensor = MagicMock()
        mock_sensor.key = "living_room"
        with patch('stations.home_assistant.get_value') as mock_value:
            with patch('stations.home_assistant.get_occupancy') as mock_occ:
                mock_value.return_value = 72.5
                mock_occ.return_value = 1
                home_assistant.populate_ecobee_sensor("token", mock_sensor, MagicMock())
                self.assertEqual(mock_sensor.temperature, 72.5)
                self.assertEqual(mock_sensor.occupied, 1)

    def test_populate_ecobee_thermostat(self):
        """Test populating ecobee thermostat with full data."""
        mock_sensor = MagicMock()
        mock_sensor.key = "climate.living_room"
        sensor_data = {
            "attributes": {
                "target_temp_high": 75,
                "target_temp_low": 68,
                "current_humidity": 45,
                "fan_mode": "auto",
                "current_temperature": 72.5,
                "hvac_action": "heating",
                "preset_mode": "home"
            },
            "state": "heat"
        }
        with patch('stations.home_assistant.get_sensor_data') as mock_data:
            with patch('stations.home_assistant.get_occupancy') as mock_occ:
                mock_data.return_value = sensor_data
                mock_occ.return_value = 1
                home_assistant.populate_ecobee_thermostat("token", mock_sensor, MagicMock())
                self.assertEqual(mock_sensor.heat_set, 75)
                self.assertEqual(mock_sensor.cool_set, 68)
                self.assertEqual(mock_sensor.humidity, 45)
                self.assertEqual(mock_sensor.temperature, 72.5)

    def test_populate_ecobee_thermostat_none(self):
        """Test populate_ecobee_thermostat with None sensor data."""
        mock_sensor = MagicMock()
        with patch('stations.home_assistant.get_sensor_data') as mock_data:
            mock_data.return_value = None
            home_assistant.populate_ecobee_thermostat("token", mock_sensor, MagicMock())
            # Function should return early without setting attributes

    def test_populate_ecobee_thermostat_off(self):
        """Test ecobee thermostat mode when turned off."""
        mock_sensor = MagicMock()
        mock_sensor.key = "climate.living_room"
        sensor_data = {
            "attributes": {
                "target_temp_high": 75,
                "target_temp_low": 68,
                "current_humidity": 45,
                "fan_mode": "auto",
                "current_temperature": 72.5,
                "hvac_action": "off",
                "preset_mode": "home"
            },
            "state": "off"
        }
        with patch('stations.home_assistant.get_sensor_data') as mock_data:
            with patch('stations.home_assistant.get_occupancy') as mock_occ:
                mock_data.return_value = sensor_data
                mock_occ.return_value = 0
                home_assistant.populate_ecobee_thermostat("token", mock_sensor, MagicMock())
                self.assertEqual(mock_sensor.mode, "Off")

    def test_populate_ecobee_thermostat_override(self):
        """Test ecobee thermostat mode when in override."""
        mock_sensor = MagicMock()
        mock_sensor.key = "climate.living_room"
        sensor_data = {
            "attributes": {
                "target_temp_high": 75,
                "target_temp_low": 68,
                "current_humidity": 45,
                "fan_mode": "auto",
                "current_temperature": 72.5,
                "hvac_action": "heating",
                "preset_mode": "temp"
            },
            "state": "heat"
        }
        with patch('stations.home_assistant.get_sensor_data') as mock_data:
            with patch('stations.home_assistant.get_occupancy') as mock_occ:
                mock_data.return_value = sensor_data
                mock_occ.return_value = 0
                home_assistant.populate_ecobee_thermostat("token", mock_sensor, MagicMock())
                self.assertEqual(mock_sensor.mode, "Override")

if __name__ == '__main__':
    unittest.main()
