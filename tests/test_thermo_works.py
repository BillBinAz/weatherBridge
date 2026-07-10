import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from stations.thermo_works import thermo_works
from weather import data


class TestThermoWorks(unittest.TestCase):

    @patch('stations.thermo_works.thermo_works.get_devices_for_user')
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    def test_get_weather_success(self, mock_loop, mock_get_devices):
        """Test successful weather data retrieval from ThermoWorks."""
        # Mock the async parts
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()
        mock_task.result.return_value = ([], {})  # No devices
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop.return_value = mock_loop_instance

        home = data.Home()
        thermo_works.get_weather(home)

        # Should not crash
        self.assertIsNotNone(home)

    def test_check_types_valid(self):
        """Test check_types with valid thermoworks type."""
        result = thermo_works.check_types("7|1|key|label")
        self.assertTrue(result)

    def test_check_types_zero(self):
        """Test check_types with type 0 (always valid)."""
        result = thermo_works.check_types("0|1|key|label")
        self.assertTrue(result)

    def test_check_types_invalid(self):
        """Test check_types with invalid type."""
        result = thermo_works.check_types("99|1|key|label")
        self.assertFalse(result)

    def test_check_types_humidity_type(self):
        """Test check_types with humidity thermoworks type."""
        result = thermo_works.check_types("8|1|key|label")
        self.assertTrue(result)

    def test_check_types_two_channel_type(self):
        """Test check_types with two-channel thermoworks type."""
        result = thermo_works.check_types("9|1|key|label")
        self.assertTrue(result)

    def test_get_sensor_by_key_found(self):
        """Test get_sensor_by_key when sensor is found."""
        sensors = [MagicMock(key="device1"), MagicMock(key="device2")]
        result = thermo_works.get_sensor_by_key(sensors, "device1")
        self.assertEqual(result, sensors[0])

    def test_get_sensor_by_key_not_found(self):
        """Test get_sensor_by_key when sensor is not found."""
        sensors = [MagicMock(key="device1"), MagicMock(key="device2")]
        result = thermo_works.get_sensor_by_key(sensors, "device3")
        self.assertIsNone(result)

    def test_get_sensor_by_key_empty_list(self):
        """Test get_sensor_by_key with empty sensor list."""
        result = thermo_works.get_sensor_by_key([], "device1")
        self.assertIsNone(result)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {})
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    def test_get_weather_no_sensors_configured(self, mock_loop):
        """Test get_weather with no sensors configured."""
        home = data.Home()
        thermo_works.get_weather(home)

        self.assertIsNotNone(home)
        self.assertEqual(len(home.climate.sensors), 0)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '7|1|device1|label'})
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    def test_get_weather_device_without_device_id(self, mock_loop):
        """Test get_weather with device that has no device_id."""
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()

        # Create mock device with no device_id
        mock_device = MagicMock(serial="serial1", device_id=None)
        device_channels_by_device = {"serial1": []}

        mock_task.result.return_value = ([mock_device], device_channels_by_device)
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop_instance.run_until_complete.return_value = None
        mock_loop.return_value = mock_loop_instance

        home = data.Home()
        thermo_works.get_weather(home)

        # Device without device_id should be skipped
        self.assertEqual(len(home.climate.sensors), 0)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '7|1|device2|label'})
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    def test_get_weather_no_matching_sensor(self, mock_loop):
        """Test get_weather when device doesn't match any configured sensor."""
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()

        # Create mock device with non-matching device_id
        mock_device = MagicMock(serial="serial1", device_id="device1")
        device_channels_by_device = {"serial1": []}

        mock_task.result.return_value = ([mock_device], device_channels_by_device)
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop_instance.run_until_complete.return_value = None
        mock_loop.return_value = mock_loop_instance

        home = data.Home()
        thermo_works.get_weather(home)

        # No matching sensor should result in no sensors added
        self.assertEqual(len(home.climate.sensors), 0)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '7|1|device1|label'})
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    def test_get_weather_exception_handling(self, mock_loop):
        """Test get_weather exception handling."""
        mock_loop.side_effect = Exception("Event loop error")

        home = data.Home()
        # Should not raise exception
        thermo_works.get_weather(home)

        self.assertIsNotNone(home)

    def test_check_types_multiple_valid_types(self):
        """Test check_types recognizes all valid thermoworks types."""
        valid_types = [
            ("7|1|key|label", True),   # CLIMATE_TYPE_THERMOWORKS_NODE
            ("8|1|key|label", True),   # CLIMATE_TYPE_THERMOWORKS_NODE_WITH_HUMIDITY
            ("9|1|key|label", True),   # CLIMATE_TYPE_THERMOWORKS_NODE_TWO_CHANNEL
            ("0|1|key|label", True),   # Always valid
            ("6|1|key|label", False),  # Invalid type
            ("10|1|key|label", False), # Invalid type
        ]
        for config, expected in valid_types:
            with self.subTest(config=config):
                result = thermo_works.check_types(config)
                self.assertEqual(result, expected)

    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    def test_get_weather_handles_assertion_error(self, mock_loop):
        """Test get_weather handles assertion errors from devices without serial."""
        mock_loop.side_effect = AssertionError("No serial found")

        home = data.Home()
        # Should not raise exception, handled in try-except
        thermo_works.get_weather(home)

        self.assertIsNotNone(home)

if __name__ == '__main__':
    unittest.main()
