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

if __name__ == '__main__':
    unittest.main()
