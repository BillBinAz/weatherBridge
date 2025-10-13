from typing import Dict
from aiohttp import ClientSession
from thermoworks_cloud import AuthFactory, ThermoworksCloud, ResourceNotFoundError
from thermoworks_cloud.models.device import Device
from thermoworks_cloud.models.device_channel import DeviceChannel
import utilities.connect as connect

CONNECT_ITEM_ID = "ca5blc76voyvw3n347z6k3fj3y"

async def get_devices_for_user():
    # Use a context manager when providing the session to the auth factory
    async with ClientSession() as session:
        #
        # Get security data
        credentials = connect.get_credentials(CONNECT_ITEM_ID)
        user_name = credentials[0].value
        password = credentials[1].value

        auth = await AuthFactory(session).build_auth(user_name, password)
        thermoworks = ThermoworksCloud(auth)
        user = await thermoworks.get_user()
        if not user.account_id:
            raise RuntimeError("No account ID found for user")

        devices = await thermoworks.get_devices(user.account_id)
        device_channels_by_device: dict[str, list[DeviceChannel]] = {}

        # Collect Data
        for device in devices:
            if not device.serial:
                continue

            try:
                device_channels = []

                # According to reverse engineering, channels seem to be 1 indexed
                for channel in range(1, 10):
                    try:
                        device_channels.append(
                            await thermoworks.get_device_channel(
                                device_serial=device.serial, channel=str(
                                    channel)
                            )
                        )
                    except ResourceNotFoundError:
                        # Go until there are no more
                        break
                    except Exception as e:
                        print(
                            f"Error getting channel {channel} for device {device.serial}: {e}")
                        continue

                device_channels_by_device[device.serial] = device_channels
            except Exception as e:
                print(f"Error getting device {device.serial}: {e}")
                continue

        # Group devices by type
        devices_by_type: Dict[str, list[Device]] = {}
        for device in devices:
            device_type = device.type or "unknown"
            if device_type not in devices_by_type:
                devices_by_type[device_type] = []
            devices_by_type[device_type].append(device)

        return devices, device_channels_by_device