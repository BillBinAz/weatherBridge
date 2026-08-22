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

    def test_get_alarm_label_passthrough_states(self):
        """Test alarm label display formatting for Home Assistant alarm states."""
        test_cases = [
            ("disarmed", "Disarmed"),
            ("arming", "Arming"),
            ("triggered", "Triggered"),
            ("armed_home", "Armed Home"),
            ("armed_night", "Armed Night"),
            ("armed_away", "Armed Away"),
        ]

        for state, expected in test_cases:
            with self.subTest(state=state):
                with patch('stations.home_assistant.get_sensor_data') as mock_get:
                    mock_get.return_value = {"state": state}
                    result = home_assistant.get_alarm_label("token", "entity", MagicMock())
                    self.assertEqual(result, expected)

    def test_get_alarm_label_none(self):
        """Test alarm label when sensor data is None."""
        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = None
            result = home_assistant.get_alarm_label("token", "entity", MagicMock())
            self.assertEqual(result, "Disarmed")

    def test_get_alarm_status_armed(self):
        """Test alarm status when armed."""
        result = home_assistant.get_alarm_status("Armed away")
        self.assertEqual(result, 1)

    def test_get_alarm_status_disarmed(self):
        """Test alarm status when disarmed."""
        result = home_assistant.get_alarm_status("Disarmed")
        self.assertEqual(result, 0)

    def test_get_alarm_status_disarmed_mixed_case(self):
        """Test alarm status when disarmed label uses mixed case."""
        result = home_assistant.get_alarm_status("dIsArMeD")
        self.assertEqual(result, 0)

    def test_get_alarm_status_none(self):
        """Test alarm status when alarm label is None."""
        result = home_assistant.get_alarm_status(None)
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
                self.assertEqual(mock_sensor.heat_set, 68)
                self.assertEqual(mock_sensor.cool_set, 75)
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

    def test_add_climate_sensor_humidity(self):
        """Test adding humidity climate sensor."""
        mock_home = MagicMock()
        mock_sensor = MagicMock(type=11, key="humidity_sensor")
        mock_home.climate.create_sensor.return_value = mock_sensor

        sensor_data = {
            "attributes": {
                "current_humidity": 55.0,
                "humidity": 60.0
            },
            "state": "on"
        }

        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = sensor_data
            result = home_assistant.add_climate_sensor("token", "11|1|humidity_sensor|label", mock_home, 0, 0, MagicMock())
            self.assertEqual(result, mock_sensor)
            self.assertEqual(mock_sensor.humidity, 55.0)

    def test_add_climate_sensor_humidity_mode(self):
        """Test adding humidity sensor uses mode when present."""
        mock_home = MagicMock()
        mock_sensor = MagicMock(type=11, key="humidity_sensor")
        mock_home.climate.create_sensor.return_value = mock_sensor

        sensor_data = {
            "attributes": {
                "current_humidity": 55.0,
                "humidity": 60.0,
                "mode": "auto"
            },
            "state": "on"
        }

        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = sensor_data
            result = home_assistant.add_climate_sensor("token", "11|1|humidity_sensor|label", mock_home, 0, 0, MagicMock())
            self.assertEqual(result, mock_sensor)
            self.assertEqual(mock_sensor.mode, "Auto")

    def test_add_climate_sensor_humidity_equipment_status(self):
        """Test adding humidity sensor uses equipment_status when mode is absent."""
        mock_home = MagicMock()
        mock_sensor = MagicMock(type=11, key="humidity_sensor")
        mock_home.climate.create_sensor.return_value = mock_sensor

        sensor_data = {
            "attributes": {
                "current_humidity": 55.0,
                "humidity": 60.0,
                "equipment_status": "heating"
            },
            "state": "on"
        }

        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = sensor_data
            result = home_assistant.add_climate_sensor("token", "11|1|humidity_sensor|label", mock_home, 0, 0, MagicMock())
            self.assertEqual(result, mock_sensor)
            self.assertEqual(mock_sensor.mode, "Heating")

    def test_add_climate_sensor_humidity_state_fallback(self):
        """Test adding humidity sensor falls back to state when no mode fields exist."""
        mock_home = MagicMock()
        mock_sensor = MagicMock(type=11, key="humidity_sensor")
        mock_home.climate.create_sensor.return_value = mock_sensor

        sensor_data = {
            "attributes": {
                "current_humidity": 55.0,
                "humidity": 60.0
            },
            "state": "on"
        }

        with patch('stations.home_assistant.get_sensor_data') as mock_get:
            mock_get.return_value = sensor_data
            result = home_assistant.add_climate_sensor("token", "11|1|humidity_sensor|label", mock_home, 0, 0, MagicMock())
            self.assertEqual(result, mock_sensor)
            self.assertEqual(mock_sensor.mode, "on")

    def test_add_climate_sensor_ecobee_thermostat(self):
        """Test adding ecobee thermostat climate sensor."""
        mock_home = MagicMock()
        mock_sensor = MagicMock(type=5, key="thermostat")
        mock_home.climate.create_sensor.return_value = mock_sensor

        with patch('stations.home_assistant.populate_ecobee_thermostat') as mock_populate:
            result = home_assistant.add_climate_sensor("token", "5|1|thermostat|label", mock_home, 0, 0, MagicMock())
            self.assertEqual(result, mock_sensor)
            mock_populate.assert_called_once()

    def test_add_climate_sensor_ecobee_sensor(self):
        """Test adding ecobee sensor climate sensor."""
        mock_home = MagicMock()
        mock_sensor = MagicMock(type=6, key="sensor")
        mock_home.climate.create_sensor.return_value = mock_sensor

        with patch('stations.home_assistant.populate_ecobee_sensor') as mock_populate:
            result = home_assistant.add_climate_sensor("token", "6|1|sensor|label", mock_home, 0, 0, MagicMock())
            self.assertEqual(result, mock_sensor)
            mock_populate.assert_called_once()

    def test_add_climate_sensor_unknown_type(self):
        """Test adding climate sensor with unknown type."""
        mock_home = MagicMock()
        mock_sensor = MagicMock(type=99)
        mock_home.climate.create_sensor.return_value = mock_sensor

        result = home_assistant.add_climate_sensor("token", "99|1|unknown|label", mock_home, 0, 0, MagicMock())
        self.assertIsNone(result)

    def test_add_alarm_zone_contact(self):
        """Test adding contact alarm zone."""
        mock_home = MagicMock()
        mock_home.alarm.all_zones_closed = 1
        
        with patch('stations.home_assistant.get_on_off_state') as mock_state:
            mock_state.return_value = 1
            home_assistant.add_alarm_zone("token", "0|1|contact_sensor|Living Room", mock_home, MagicMock())
            mock_home.alarm.zones.append.assert_called_once()
            self.assertEqual(mock_home.alarm.all_zones_closed, 1)

    def test_add_alarm_zone_motion(self):
        """Test adding motion alarm zone."""
        mock_home = MagicMock()
        
        with patch('stations.home_assistant.get_on_off_state') as mock_state:
            mock_state.return_value = 0
            home_assistant.add_alarm_zone("token", "1|1|motion_sensor|Living Room", mock_home, MagicMock())
            mock_home.alarm.zones.append.assert_called_once()

    def test_add_alarm_zone_garage_door(self):
        """Test adding garage door alarm zone."""
        mock_home = MagicMock()
        
        with patch('stations.home_assistant.get_on_off_state') as mock_state:
            mock_state.return_value = 1
            home_assistant.add_alarm_zone("token", "3|1|garage_door|Garage Door", mock_home, MagicMock())
            mock_home.alarm.zones.append.assert_called_once()

    def test_add_alarm_zone_door(self):
        """Test adding door alarm zone with lock."""
        mock_home = MagicMock()
        
        with patch('stations.home_assistant.get_on_off_state') as mock_state:
            with patch('stations.home_assistant.get_locked_state') as mock_lock:
                mock_state.return_value = 1
                mock_lock.return_value = 1
                home_assistant.add_alarm_zone("token", "2|1|front_door|Front Door|lock_entity", mock_home, MagicMock())
                mock_home.alarm.zones.append.assert_called_once()
                mock_home.doors.append.assert_called_once()

    def test_add_alarm_zone_contact_open(self):
        """Test adding contact alarm zone that is open."""
        mock_home = MagicMock()
        mock_home.alarm.all_zones_closed = 1
        
        with patch('stations.home_assistant.get_on_off_state') as mock_state:
            mock_state.return_value = 0  # Open/not safe
            home_assistant.add_alarm_zone("token", "0|1|contact_sensor|Living Room", mock_home, MagicMock())
            self.assertEqual(mock_home.alarm.all_zones_closed, 0)

    def test_add_alarm_zone_does_not_reset_open_contact_state(self):
        """Test later zones do not reset an open contact state."""
        mock_home = MagicMock()
        mock_home.alarm.all_zones_closed = 1

        with patch('stations.home_assistant.get_on_off_state') as mock_state:
            mock_state.side_effect = [0, 1]
            home_assistant.add_alarm_zone("token", "0|1|contact_sensor|Living Room", mock_home, MagicMock())
            home_assistant.add_alarm_zone("token", "1|2|motion_sensor|Hallway", mock_home, MagicMock())

        self.assertEqual(mock_home.alarm.all_zones_closed, 0)

    @patch.dict('stations.home_assistant.os.environ', {})
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    def test_get_weather_no_bearer_token(self, mock_token, mock_session):
        """Test get_weather when bearer token is missing."""
        mock_token.return_value = None
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        home = data.Home()
        home_assistant.get_weather(home)

        # Should handle gracefully
        self.assertIsNotNone(home)

    @patch.dict('stations.home_assistant.os.environ', {'ALARM_ZONE_1': '0|1|contact|Living Room', 'CLIMATE_SENSOR_1': '5|1|thermostat|Main'})
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    @patch('stations.home_assistant.add_alarm_zone')
    @patch('stations.home_assistant.add_climate_sensor')
    def test_get_weather_with_alarm_and_climate(self, mock_climate, mock_alarm, mock_token, mock_session):
        """Test get_weather with both alarm zones and climate sensors."""
        mock_token.return_value = "token"
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        mock_sensor = MagicMock(type=5, temperature="72.5")
        mock_climate.return_value = mock_sensor

        with patch('stations.home_assistant.get_alarm_status') as mock_status:
            with patch('stations.home_assistant.get_alarm_label') as mock_label:
                mock_status.return_value = 1
                mock_label.return_value = "Armed"
                
                home = data.Home()
                home_assistant.get_weather(home)

                self.assertIsNotNone(home)

    @patch.dict('stations.home_assistant.os.environ', {'CLIMATE_SENSOR_1': '5|1|thermostat|Main', 'CLIMATE_SENSOR_2': '6|1|sensor|Bedroom'})
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    @patch('stations.home_assistant.add_climate_sensor')
    def test_get_weather_multiple_climate_sensors(self, mock_add_sensor, mock_token, mock_session):
        """Test get_weather with multiple climate sensors for averaging."""
        mock_token.return_value = "token"
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance
        
        # Create mock sensors with temperatures
        mock_sensor1 = MagicMock(type=5, temperature="72.0")
        mock_sensor2 = MagicMock(type=6, temperature="70.0")
        mock_add_sensor.side_effect = [mock_sensor1, mock_sensor2]

        home = data.Home()
        home_assistant.get_weather(home)

        self.assertIsNotNone(home)

    @patch.dict('stations.home_assistant.os.environ', {'CLIMATE_SENSOR_1': '5|1|thermostat|Main', 'CLIMATE_SENSOR_2': '6|1|sensor|Bedroom'})
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    @patch('stations.home_assistant.add_climate_sensor')
    def test_get_weather_continues_after_sensor_failure(self, mock_add_sensor, mock_token, mock_session):
        """Test get_weather keeps processing later climate sensors after one fails."""
        mock_token.return_value = "token"
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_sensor = MagicMock(type=6, temperature="70.0")
        mock_add_sensor.side_effect = [Exception("bad sensor"), mock_sensor]

        home = data.Home()
        home_assistant.get_weather(home)

        self.assertIsNotNone(home)
        self.assertEqual(mock_add_sensor.call_count, 2)
        self.assertEqual(len(home.climate.sensors), 1)

    @patch.dict('stations.home_assistant.os.environ', {'ALARM_ZONE_1': '0|1|contact|Living Room', 'CLIMATE_SENSOR_1': '5|1|thermostat|Main'})
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    @patch('stations.home_assistant.add_alarm_zone')
    @patch('stations.home_assistant.add_climate_sensor')
    def test_get_weather_continues_after_alarm_zone_failure(self, mock_climate, mock_alarm, mock_token, mock_session):
        """Test get_weather keeps processing climate sensors after an alarm zone fails."""
        mock_token.return_value = "token"
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        mock_sensor = MagicMock(type=5, temperature="72.5")
        mock_alarm.side_effect = [Exception("bad zone")]
        mock_climate.return_value = mock_sensor

        home = data.Home()
        home_assistant.get_weather(home)

        self.assertIsNotNone(home)
        self.assertEqual(mock_alarm.call_count, 1)
        self.assertEqual(mock_climate.call_count, 1)
        self.assertEqual(len(home.climate.sensors), 1)
    @patch.dict('stations.home_assistant.os.environ', {'CLIMATE_SENSOR_1': '5|1|thermostat|Main'})
    @patch('stations.home_assistant.requests.Session')
    @patch('stations.home_assistant.get_bearer_token')
    def test_get_weather_sensor_without_temperature(self, mock_token, mock_session):
        """Test get_weather when sensor temperature is DEFAULT_TEMPERATURE."""
        mock_token.return_value = "token"
        mock_session_instance = MagicMock()
        mock_session.return_value = mock_session_instance

        with patch('stations.home_assistant.add_climate_sensor') as mock_add:
            mock_sensor = MagicMock(type=5, temperature='None')  # DEFAULT_TEMPERATURE
            mock_add.return_value = mock_sensor
            
            home = data.Home()
            home_assistant.get_weather(home)

            self.assertIsNotNone(home)

    def test_get_sensor_data_empty_response(self):
        """Test get_sensor_data with empty response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = '{}'
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response

        with patch('stations.home_assistant.HOME_ASSISTANT_URL', 'http://test.com/'):
            result = home_assistant.get_sensor_data("token", "entity", mock_session)
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
