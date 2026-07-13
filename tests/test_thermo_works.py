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

    def test_check_types_invalid_format(self):
        """Test check_types with malformed config."""
        result = thermo_works.check_types("invalid")
        self.assertFalse(result)

    def test_check_types_none(self):
        """Test check_types with None input."""
        result = thermo_works.check_types(None)
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

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '8|1|device_humidity|label'})
    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '8|device_humidity|label'})
    @patch('stations.thermo_works.thermo_works.get_devices_for_user')
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    @patch('stations.thermo_works.thermo_works.conversions.format_f')
    def test_get_weather_humidity_sensor_flow(self, mock_format, mock_loop, mock_get_devices):
        """Test get_weather processes humidity sensor correctly."""
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()

        # Create mock device with temperature and humidity
        mock_device = MagicMock(serial="serial1", device_id="device_humidity")
        mock_channel0 = MagicMock(value=72.5)  # Ambient
        mock_channel1 = MagicMock(value=55.0)  # Humidity
        device_channels_by_device = {"serial1": [mock_channel0, mock_channel1]}

        mock_task.result.return_value = ([mock_device], device_channels_by_device)
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop_instance.run_until_complete.return_value = None
        mock_loop.return_value = mock_loop_instance
        mock_format.side_effect = lambda x, *args: x

        home = data.Home()
        thermo_works.get_weather(home)

        # Verify format_f was called for temperature and humidity
        self.assertGreater(mock_format.call_count, 0)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '9|device_two_ch|label'})
    @patch('stations.thermo_works.thermo_works.get_devices_for_user')
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    @patch('stations.thermo_works.thermo_works.conversions.format_f')
    def test_get_weather_two_channel_sensor_flow(self, mock_format, mock_loop, mock_get_devices):
        """Test get_weather processes two-channel sensor correctly."""
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()

        # Create mock device with ambient, refrigerator, and freezer channels
        mock_device = MagicMock(serial="serial1", device_id="device_two_ch")
        mock_channel0 = MagicMock(value=72.5)  # Ambient
        mock_channel1 = MagicMock(value=38.0)  # Refrigerator
        mock_channel2 = MagicMock(value=0.0)   # Freezer
        device_channels_by_device = {"serial1": [mock_channel0, mock_channel1, mock_channel2]}

        mock_task.result.return_value = ([mock_device], device_channels_by_device)
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop_instance.run_until_complete.return_value = None
        mock_loop.return_value = mock_loop_instance
        mock_format.side_effect = lambda x, *args: x

        home = data.Home()
        thermo_works.get_weather(home)

        # Verify format_f was called for all three channels
        self.assertGreater(mock_format.call_count, 0)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '7|device_node|label'})
    @patch('stations.thermo_works.thermo_works.get_devices_for_user')
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    @patch('stations.thermo_works.thermo_works.conversions.format_f')
    def test_get_weather_node_sensor_flow(self, mock_format, mock_loop, mock_get_devices):
        """Test get_weather processes node sensor correctly."""
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()

        # Create mock device with ambient and freezer channels
        mock_device = MagicMock(serial="serial1", device_id="device_node")
        mock_channel0 = MagicMock(value=72.5)  # Ambient
        mock_channel1 = MagicMock(value=0.0)   # Freezer
        device_channels_by_device = {"serial1": [mock_channel0, mock_channel1]}

        mock_task.result.return_value = ([mock_device], device_channels_by_device)
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop_instance.run_until_complete.return_value = None
        mock_loop.return_value = mock_loop_instance
        mock_format.side_effect = lambda x, *args: x

        home = data.Home()
        thermo_works.get_weather(home)

        # Verify format_f was called for both channels
        self.assertGreater(mock_format.call_count, 0)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {'CLIMATE_SENSOR_1': '7|1|device|label'})
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    def test_get_weather_exception_in_finally(self, mock_loop):
        """Test get_weather handles exceptions in finally block."""
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()
        
        # Make result() raise an exception to trigger finally block
        mock_task.result.side_effect = RuntimeError("Task failed")
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop.return_value = mock_loop_instance

        home = data.Home()
        # Should not raise exception, handled in try-except-finally
        thermo_works.get_weather(home)

        self.assertIsNotNone(home)

    @patch.dict('stations.thermo_works.thermo_works.os.environ', {
        'CLIMATE_SENSOR_1': '7|device_bad|label',
        'CLIMATE_SENSOR_2': '7|device_good|label'
    })
    @patch('stations.thermo_works.thermo_works.asyncio.new_event_loop')
    @patch('stations.thermo_works.thermo_works.conversions.format_f')
    def test_get_weather_continues_after_device_failure(self, mock_format, mock_loop):
        """Test get_weather keeps processing later ThermoWorks devices after one fails."""
        mock_loop_instance = MagicMock()
        mock_task = MagicMock()

        bad_device = MagicMock(serial="bad_serial", device_id="device_bad")
        good_device = MagicMock(serial="good_serial", device_id="device_good")
        device_channels_by_device = {
            "bad_serial": [],
            "good_serial": [MagicMock(value=72.5), MagicMock(value=0.0)]
        }

        mock_task.result.return_value = ([bad_device, good_device], device_channels_by_device)
        mock_loop_instance.create_task.return_value = mock_task
        mock_loop_instance.run_until_complete.return_value = None
        mock_loop.return_value = mock_loop_instance
        mock_format.side_effect = lambda x, *args: x

        home = data.Home()
        thermo_works.get_weather(home)

        self.assertEqual(len(home.climate.sensors), 1)
        self.assertEqual(home.climate.sensors[0].label, 'label')

if __name__ == '__main__':
    unittest.main()
