import asyncio
import logging
import pprint
from dataclasses import asdict
from thermoworks_cloud.models.device import Device
from thermoworks_cloud.models.device_channel import DeviceChannel
from weather import stations
import datetime as dt

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


def main():
    try:
        logging.basicConfig(format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                            datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)

        loop = asyncio.new_event_loop()
        task = loop.create_task(stations.thermo_works.get_devices_for_user())
        loop.run_until_complete(task)
        results = task.result()
        devices = results[0]
        device_channels_by_device = results[1]

        for device in devices:
            device_channels = device_channels_by_device.get(device.serial, [])
            print_device_info(device, device_channels)

    except Exception as e:
        logging.error("Unable to update IoX " + str(e))
        print(dt.datetime.now().time(), "Unable to update IoX " + str(e))


main()
