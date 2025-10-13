import pprint
from dataclasses import asdict
from typing import Dict

from aiohttp import ClientSession

from thermoworks_cloud import AuthFactory, ThermoworksCloud, ResourceNotFoundError
from thermoworks_cloud.models.device import Device
from thermoworks_cloud.models.device_channel import DeviceChannel
import utilities.connect as connect
import utilities.conversions as conversions

# Make sure these are defined
CONNECT_ITEM_ID = "ca5blc76voyvw3n347z6k3fj3y"
HUMIDOR_NODE_ID = 'B0:A7:32:C5:5A:74'
SAFE_NODE_ID = '08:F9:E0:95:B9:20'
KITCHEN_NODE_ID = 'B0:A7:32:CA:4B:F4'
GARAGE_NODE_ID = '10:06:1C:A6:4A:90'

def print_device_info(device: Device, device_channels: list[DeviceChannel]):
    """Print detailed information about a device and its channels."""
    device_dict = asdict(device)

    print(f"\n{'=' * 50}")
    print(f"DEVICE TYPE: {device.type or 'Unknown'}")
    print(f"DEVICE NAME: {device.label or 'Unnamed'}")
    print(f"SERIAL: {device.serial or 'Unknown'}")
    print(f"{'=' * 50}")

    # Print all device properties
    print("\nDEVICE PROPERTIES:")
    pprint.pprint(device_dict, compact=False)

    # Print channel information
    if device_channels:
        print(f"\nCHANNELS ({len(device_channels)}):")
        for i, channel in enumerate(device_channels):
            channel_dict = asdict(channel)
            print(f"\n  Channel {i+1}:")
            pprint.pprint(channel_dict)
    else:
        print("\nNo channels found for this device.")


async def get_devices_for_user(weather_data):
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

        # Print detailed information for each device
        for device in devices:
            assert device.serial is not None
            device_channels = device_channels_by_device.get(device.serial, [])

            # SAFE 0: Ambient, 1: Humidity
            if device.device_id == SAFE_NODE_ID:
                weather_data.safe.temp  = conversions.format_f(device_channels[0].value)
                weather_data.safe.temp_c = conversions.f_to_c(device_channels[0].value)
                weather_data.safe.humidity = conversions.format_f(device_channels[1].value)

            # KITCHEN 0: Ambient, 1: Refrigerator, 2: Freezer
            if device.device_id == KITCHEN_NODE_ID:
                weather_data.kitchen.temp  = conversions.format_f(device_channels[0].value)
                weather_data.kitchen.temp_c = conversions.f_to_c(device_channels[0].value)

                weather_data.kitchen_refrigerator.temp  = conversions.format_f(device_channels[1].value)
                weather_data.kitchen_refrigerator.temp_c = conversions.f_to_c(device_channels[1].value)

                weather_data.kitchen_freezer.temp  = conversions.format_f(device_channels[2].value)
                weather_data.kitchen_freezer.temp_c = conversions.f_to_c(device_channels[2].value)

            # GARAGE 0: Ambient, 1: Freezer
            if device.device_id == GARAGE_NODE_ID:
                weather_data.garage.temp  = conversions.format_f(device_channels[0].value)
                weather_data.garage.temp_c = conversions.f_to_c(device_channels[0].value)

                weather_data.garage_freezer.temp  = conversions.format_f(device_channels[1].value)
                weather_data.garage_freezer.temp_c = conversions.f_to_c(device_channels[1].value)

            # HUMIDOR 0: Ambient, 1: Humidity
            if device.device_id == HUMIDOR_NODE_ID:
                weather_data.humidor.temp  = conversions.format_f(device_channels[0].value)
                weather_data.humidor.temp_c = conversions.f_to_c(device_channels[0].value)
                weather_data.humidor.humidity = conversions.format_f(device_channels[1].value)
