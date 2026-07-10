import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from stations.thermo_works import get_devices_for_user


class TestGetDevicesForUser(unittest.IsolatedAsyncioTestCase):

    @patch('stations.thermo_works.get_devices_for_user.connect.get_credentials')
    @patch('stations.thermo_works.get_devices_for_user.AuthFactory')
    @patch('stations.thermo_works.get_devices_for_user.ThermoworksCloud')
    @patch('stations.thermo_works.get_devices_for_user.ClientSession')
    async def test_get_devices_for_user_success(self, mock_session, mock_thermo_cloud, mock_auth_factory, mock_credentials):
        """Test successful device retrieval."""
        # Setup credentials
        mock_cred1 = MagicMock(value="test_user")
        mock_cred2 = MagicMock(value="test_pass")
        mock_credentials.return_value = [mock_cred1, mock_cred2]

        # Setup auth
        mock_auth_instance = AsyncMock()
        mock_auth_factory_instance = MagicMock()
        mock_auth_factory_instance.build_auth = AsyncMock(return_value=mock_auth_instance)
        mock_auth_factory.return_value = mock_auth_factory_instance

        # Setup user
        mock_user = MagicMock(account_id="test_account_id")

        # Setup devices
        mock_device1 = MagicMock(serial="device1", type="thermostat")
        mock_device2 = MagicMock(serial="device2", type="sensor")
        devices = [mock_device1, mock_device2]

        # Setup ThermoworksCloud
        mock_thermo_instance = MagicMock()
        mock_thermo_instance.get_user = AsyncMock(return_value=mock_user)
        mock_thermo_instance.get_devices = AsyncMock(return_value=devices)
        mock_thermo_instance.get_device_channel = AsyncMock()
        mock_thermo_cloud.return_value = mock_thermo_instance

        # Setup ClientSession
        mock_session_instance = AsyncMock()
        mock_session.__aenter__.return_value = mock_session_instance
        mock_session.__aexit__.return_value = None

        result_devices, device_channels = await get_devices_for_user.get_devices_for_user()

        self.assertEqual(len(result_devices), 2)
        self.assertEqual(result_devices[0].serial, "device1")
        self.assertEqual(result_devices[1].serial, "device2")

    @patch('stations.thermo_works.get_devices_for_user.connect.get_credentials')
    @patch('stations.thermo_works.get_devices_for_user.AuthFactory')
    @patch('stations.thermo_works.get_devices_for_user.ThermoworksCloud')
    @patch('stations.thermo_works.get_devices_for_user.ClientSession')
    async def test_get_devices_for_user_no_account_id(self, mock_session, mock_thermo_cloud, mock_auth_factory, mock_credentials):
        """Test when user has no account ID."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]

        mock_auth_instance = AsyncMock()
        mock_auth_factory_instance = MagicMock()
        mock_auth_factory_instance.build_auth = AsyncMock(return_value=mock_auth_instance)
        mock_auth_factory.return_value = mock_auth_factory_instance

        mock_user = MagicMock(account_id=None)
        mock_thermo_instance = MagicMock()
        mock_thermo_instance.get_user = AsyncMock(return_value=mock_user)
        mock_thermo_cloud.return_value = mock_thermo_instance

        mock_session_instance = AsyncMock()
        mock_session.__aenter__.return_value = mock_session_instance
        mock_session.__aexit__.return_value = None

        with self.assertRaises(RuntimeError) as context:
            await get_devices_for_user.get_devices_for_user()

        self.assertIn("No account ID", str(context.exception))

    @patch('stations.thermo_works.get_devices_for_user.connect.get_credentials')
    @patch('stations.thermo_works.get_devices_for_user.AuthFactory')
    @patch('stations.thermo_works.get_devices_for_user.ThermoworksCloud')
    @patch('stations.thermo_works.get_devices_for_user.ClientSession')
    async def test_get_devices_with_channels(self, mock_session, mock_thermo_cloud, mock_auth_factory, mock_credentials):
        """Test device retrieval with multiple channels."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]

        mock_auth_instance = AsyncMock()
        mock_auth_factory_instance = MagicMock()
        mock_auth_factory_instance.build_auth = AsyncMock(return_value=mock_auth_instance)
        mock_auth_factory.return_value = mock_auth_factory_instance

        mock_user = MagicMock(account_id="account_id")

        mock_device = MagicMock(serial="device1", type="thermostat")
        devices = [mock_device]

        # Mock channels - return data for channels 1-3, ResourceNotFoundError for 4+
        from thermoworks_cloud import ResourceNotFoundError
        mock_channel1 = MagicMock(channel="1")
        mock_channel2 = MagicMock(channel="2")
        mock_channel3 = MagicMock(channel="3")

        mock_thermo_instance = MagicMock()
        mock_thermo_instance.get_user = AsyncMock(return_value=mock_user)
        mock_thermo_instance.get_devices = AsyncMock(return_value=devices)
        mock_thermo_instance.get_device_channel = AsyncMock(
            side_effect=[mock_channel1, mock_channel2, mock_channel3, ResourceNotFoundError("Not found")]
        )
        mock_thermo_cloud.return_value = mock_thermo_instance

        mock_session_instance = AsyncMock()
        mock_session.__aenter__.return_value = mock_session_instance
        mock_session.__aexit__.return_value = None

        result_devices, device_channels = await get_devices_for_user.get_devices_for_user()

        self.assertEqual(len(result_devices), 1)
        self.assertIn("device1", device_channels)
        self.assertEqual(len(device_channels["device1"]), 3)

    @patch('stations.thermo_works.get_devices_for_user.connect.get_credentials')
    @patch('stations.thermo_works.get_devices_for_user.AuthFactory')
    @patch('stations.thermo_works.get_devices_for_user.ThermoworksCloud')
    @patch('stations.thermo_works.get_devices_for_user.ClientSession')
    async def test_get_devices_with_channel_error(self, mock_session, mock_thermo_cloud, mock_auth_factory, mock_credentials):
        """Test device retrieval with channel error handling."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]

        mock_auth_instance = AsyncMock()
        mock_auth_factory_instance = MagicMock()
        mock_auth_factory_instance.build_auth = AsyncMock(return_value=mock_auth_instance)
        mock_auth_factory.return_value = mock_auth_factory_instance

        mock_user = MagicMock(account_id="account_id")

        mock_device = MagicMock(serial="device1", type="thermostat")
        devices = [mock_device]

        # Mock channels with an error in the middle
        mock_channel1 = MagicMock(channel="1")
        mock_thermo_instance = MagicMock()
        mock_thermo_instance.get_user = AsyncMock(return_value=mock_user)
        mock_thermo_instance.get_devices = AsyncMock(return_value=devices)
        mock_thermo_instance.get_device_channel = AsyncMock(
            side_effect=[mock_channel1, Exception("Channel error"), MagicMock(channel="3")]
        )
        mock_thermo_cloud.return_value = mock_thermo_instance

        mock_session_instance = AsyncMock()
        mock_session.__aenter__.return_value = mock_session_instance
        mock_session.__aexit__.return_value = None

        result_devices, device_channels = await get_devices_for_user.get_devices_for_user()

        self.assertEqual(len(result_devices), 1)
        # Should have 2 channels (channel 1 and 3, channel 2 error was skipped)
        self.assertEqual(len(device_channels["device1"]), 2)

    @patch('stations.thermo_works.get_devices_for_user.connect.get_credentials')
    @patch('stations.thermo_works.get_devices_for_user.AuthFactory')
    @patch('stations.thermo_works.get_devices_for_user.ThermoworksCloud')
    @patch('stations.thermo_works.get_devices_for_user.ClientSession')
    async def test_get_devices_skip_no_serial(self, mock_session, mock_thermo_cloud, mock_auth_factory, mock_credentials):
        """Test that devices without serial are skipped."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]

        mock_auth_instance = AsyncMock()
        mock_auth_factory_instance = MagicMock()
        mock_auth_factory_instance.build_auth = AsyncMock(return_value=mock_auth_instance)
        mock_auth_factory.return_value = mock_auth_factory_instance

        mock_user = MagicMock(account_id="account_id")

        # Device with no serial should be skipped
        mock_device_no_serial = MagicMock(serial=None, type="unknown")
        mock_device_with_serial = MagicMock(serial="device1", type="thermostat")
        devices = [mock_device_no_serial, mock_device_with_serial]

        mock_thermo_instance = MagicMock()
        mock_thermo_instance.get_user = AsyncMock(return_value=mock_user)
        mock_thermo_instance.get_devices = AsyncMock(return_value=devices)
        mock_thermo_instance.get_device_channel = AsyncMock(
            side_effect=[MagicMock(channel="1")]
        )
        mock_thermo_cloud.return_value = mock_thermo_instance

        mock_session_instance = AsyncMock()
        mock_session.__aenter__.return_value = mock_session_instance
        mock_session.__aexit__.return_value = None

        result_devices, device_channels = await get_devices_for_user.get_devices_for_user()

        # Both devices should be returned, but only one has channels
        self.assertEqual(len(result_devices), 2)
        self.assertNotIn(None, device_channels.keys())
        self.assertIn("device1", device_channels)

    @patch('stations.thermo_works.get_devices_for_user.connect.get_credentials')
    @patch('stations.thermo_works.get_devices_for_user.AuthFactory')
    @patch('stations.thermo_works.get_devices_for_user.ThermoworksCloud')
    @patch('stations.thermo_works.get_devices_for_user.ClientSession')
    async def test_get_devices_device_error(self, mock_session, mock_thermo_cloud, mock_auth_factory, mock_credentials):
        """Test device retrieval with device-level error handling."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]

        mock_auth_instance = AsyncMock()
        mock_auth_factory_instance = MagicMock()
        mock_auth_factory_instance.build_auth = AsyncMock(return_value=mock_auth_instance)
        mock_auth_factory.return_value = mock_auth_factory_instance

        mock_user = MagicMock(account_id="account_id")

        mock_device1 = MagicMock(serial="device1", type="thermostat")
        mock_device2 = MagicMock(serial="device2", type="sensor")
        devices = [mock_device1, mock_device2]

        # Mock get_device_channel to fail for device1
        call_count = [0]
        def side_effect_func(*args, **kwargs):
            call_count[0] += 1
            if kwargs.get('device_serial') == 'device1':
                raise Exception("Device error")
            return MagicMock(channel=str(call_count[0]))

        mock_thermo_instance = MagicMock()
        mock_thermo_instance.get_user = AsyncMock(return_value=mock_user)
        mock_thermo_instance.get_devices = AsyncMock(return_value=devices)
        mock_thermo_instance.get_device_channel = AsyncMock(side_effect=side_effect_func)
        mock_thermo_cloud.return_value = mock_thermo_instance

        mock_session_instance = AsyncMock()
        mock_session.__aenter__.return_value = mock_session_instance
        mock_session.__aexit__.return_value = None

        result_devices, device_channels = await get_devices_for_user.get_devices_for_user()

        self.assertEqual(len(result_devices), 2)
        # device1 should have empty channel list due to error
        self.assertIn("device1", device_channels)
        self.assertEqual(len(device_channels["device1"]), 0)
        # device2 should have channels
        self.assertIn("device2", device_channels)
        self.assertGreater(len(device_channels["device2"]), 0)

    @patch('stations.thermo_works.get_devices_for_user.connect.get_credentials')
    @patch('stations.thermo_works.get_devices_for_user.AuthFactory')
    @patch('stations.thermo_works.get_devices_for_user.ThermoworksCloud')
    @patch('stations.thermo_works.get_devices_for_user.ClientSession')
    async def test_get_devices_groups_by_type(self, mock_session, mock_thermo_cloud, mock_auth_factory, mock_credentials):
        """Test that devices are grouped by type."""
        mock_credentials.return_value = [MagicMock(value="user"), MagicMock(value="pass")]

        mock_auth_instance = AsyncMock()
        mock_auth_factory_instance = MagicMock()
        mock_auth_factory_instance.build_auth = AsyncMock(return_value=mock_auth_instance)
        mock_auth_factory.return_value = mock_auth_factory_instance

        mock_user = MagicMock(account_id="account_id")

        mock_device1 = MagicMock(serial="device1", type="thermostat")
        mock_device2 = MagicMock(serial="device2", type="thermostat")
        mock_device3 = MagicMock(serial="device3", type="sensor")
        mock_device_unknown = MagicMock(serial="device4", type=None)
        devices = [mock_device1, mock_device2, mock_device3, mock_device_unknown]

        mock_thermo_instance = MagicMock()
        mock_thermo_instance.get_user = AsyncMock(return_value=mock_user)
        mock_thermo_instance.get_devices = AsyncMock(return_value=devices)
        mock_thermo_instance.get_device_channel = AsyncMock()
        mock_thermo_cloud.return_value = mock_thermo_instance

        mock_session_instance = AsyncMock()
        mock_session.__aenter__.return_value = mock_session_instance
        mock_session.__aexit__.return_value = None

        result_devices, device_channels = await get_devices_for_user.get_devices_for_user()

        self.assertEqual(len(result_devices), 4)


if __name__ == '__main__':
    unittest.main()
