import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import MagicMock, patch

from stations import aprilaire
from weather import data


class TestAprilAire(unittest.TestCase):

    def test_check_types_valid(self):
        self.assertTrue(aprilaire.check_types("13|device|label"))

    def test_check_types_zero(self):
        self.assertTrue(aprilaire.check_types("0|device|label"))

    def test_check_types_invalid(self):
        self.assertFalse(aprilaire.check_types("99|device|label"))

    def test_check_types_invalid_format(self):
        self.assertFalse(aprilaire.check_types("invalid"))

    @patch('stations.aprilaire.Cognito')
    def test_get_id_token(self, mock_cognito):
        instance = MagicMock()
        instance.id_token = "id-token"
        mock_cognito.return_value = instance

        result = aprilaire.get_id_token("user@example.com", "secret")

        self.assertEqual(result, "id-token")
        instance.authenticate.assert_called_once_with(password="secret")

    def test_select_sensor_reading_prefers_controlling_sensor(self):
        sensors = [
            {"reading": 45, "status": "reporting"},
            {"reading": 41, "isControlling": True},
        ]
        self.assertEqual(aprilaire.select_sensor_reading(sensors), 41.0)

    def test_get_current_humidity_uses_fallback_status(self):
        primary = {"equipmentStatus": "humidifying"}
        fallback = {"currentHumidity": 38}
        self.assertEqual(aprilaire.get_current_humidity(primary, fallback), 38.0)

    @patch('stations.aprilaire.get_status_payload')
    @patch('stations.aprilaire.get_device_settings')
    @patch('stations.aprilaire.get_hierarchy_device_zones')
    @patch('stations.aprilaire.get_json')
    @patch('stations.aprilaire.get_id_token')
    @patch('stations.aprilaire.connect.get_credentials')
    @patch.dict('stations.aprilaire.os.environ', {
        'CLIMATE_SENSOR_1': '13|device-001|basement_aprilaire',
        'APRILAIRE_CONNECT_ITEM_ID': 'item-id'
    }, clear=True)
    def test_get_weather_dehumidifier(self, mock_credentials, mock_id_token, mock_get_json,
                                      mock_zones, mock_settings, mock_status):
        mock_credentials.return_value = [MagicMock(value="user@example.com"), MagicMock(value="secret")]
        mock_id_token.return_value = "token"
        mock_get_json.return_value = {"userId": "user-1"}
        mock_zones.return_value = {"device-001": "PZ1"}
        mock_settings.return_value = {
            "dehumidifier": {"mode": "on", "humiditySetpoint": 52}
        }
        mock_status.return_value = {
            "equipmentStatus": "inactive",
            "humSensors": [{"reading": 49, "isControlling": True}],
            "isCompOn": True,
            "isDehumFanOn": False,
            "isHvacFanOn": True,
            "alerts": {"highHum": False, "lowTemp": True},
            "fanTimeHours": 44,
            "filterService": {"needsService": False, "remaining": 100},
        }

        home = data.Home()
        aprilaire.get_weather(home)

        self.assertEqual(len(home.climate.sensors), 1)
        sensor = home.climate.sensors[0]
        self.assertEqual(sensor.profile, "dehumidifier")
        self.assertEqual(sensor.mode, "on")
        self.assertEqual(sensor.state, "inactive")
        self.assertEqual(sensor.humidity_set, 52.0)
        self.assertEqual(sensor.humidity, 49.0)
        self.assertTrue(sensor.isCompOn)
        self.assertFalse(sensor.isDehumFanOn)
        self.assertTrue(sensor.isHvacFanOn)
        self.assertEqual(sensor.alerts, {"highHum": False, "lowTemp": True})
        self.assertEqual(sensor.fanTimeHours, 44)
        self.assertEqual(sensor.filterService, {"needsService": False, "remaining": 100})

    @patch('stations.aprilaire.get_status_payload')
    @patch('stations.aprilaire.get_device_settings')
    @patch('stations.aprilaire.get_hierarchy_device_zones')
    @patch('stations.aprilaire.get_json')
    @patch('stations.aprilaire.get_id_token')
    @patch('stations.aprilaire.connect.get_credentials')
    @patch.dict('stations.aprilaire.os.environ', {
        'CLIMATE_SENSOR_1': '13|device-thermostat-001|whole_house_humidifier',
        'APRILAIRE_CONNECT_ITEM_ID': 'item-id'
    }, clear=True)
    def test_get_weather_attached_humidifier_uses_zone_fallback(
        self,
        mock_credentials,
        mock_id_token,
        mock_get_json,
        mock_zones,
        mock_settings,
        mock_status,
    ):
        mock_credentials.return_value = [MagicMock(value="user@example.com"), MagicMock(value="secret")]
        mock_id_token.return_value = "token"
        mock_get_json.return_value = {"userId": "user-1"}
        mock_zones.return_value = {"device-thermostat-001": "PZ1"}
        mock_settings.return_value = {
            "humidifier": {"mode": "on", "humiditySetpoint": 40}
        }
        mock_status.side_effect = [
            {"equipmentStatus": "humidifying"},
            {"currentHumidity": 38},
        ]

        home = data.Home()
        aprilaire.get_weather(home)

        self.assertEqual(len(home.climate.sensors), 1)
        sensor = home.climate.sensors[0]
        self.assertEqual(sensor.profile, "humidifier")
        self.assertEqual(sensor.mode, "on")
        self.assertEqual(sensor.state, "humidifying")
        self.assertEqual(sensor.humidity_set, 40.0)
        self.assertEqual(sensor.humidity, 38.0)


if __name__ == '__main__':
    unittest.main()
