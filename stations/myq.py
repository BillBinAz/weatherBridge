import asyncio
from aiohttp import ClientSession
import pymyq
import logging
import datetime
import sys

SECRET_FILE = "./secret/myq"
BIKE_GARAGE = 'CG08469920F5'
MAIN_GARAGE = 'CG0846887725'
MOTORCYCLE_GARAGE = 'CG0846887726'


async def async_get_myq(weather_data) -> None:

    try:

        with open(SECRET_FILE, "r") as secret_file:
            user_name = secret_file.readline().strip('\n')
            password = secret_file.readline().strip('\n')

        async with ClientSession() as web_session:
            myq = await pymyq.login(user_name, password, web_session)
            devices = myq.covers

            # Bike Garage
            weather_data.alarm.bike_garage = update(devices, BIKE_GARAGE)

            # Motorcycle Garage
            weather_data.alarm.mc_garage = update(devices, MOTORCYCLE_GARAGE)

            # Main Garage
            weather_data.alarm.main_garage = update(devices, MAIN_GARAGE)

    except Exception as e:
        logging.error("Unable to retrieve myq.covers " + str(e))
        print(datetime.datetime.now().time(), "Unable to retrieve myq.covers " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get status myq.covers " + str(e))
        print(datetime.datetime.now().time(), "Unable to get status myq.covers " + str(e))
    return


def update(devices, device_id):

    try:
        garage = devices[device_id]
        online = garage.online
        state = garage.state

        if not online:
            logging.error("Device: " + device_id + " offline")

        if state == 'closed':
            return 1
    except Exception as e:
        logging.error("Unable to get status mya:" + device_id + " " + str(e))
        print(datetime.datetime.now().time(), "Unable to get status mya:" + device_id + " " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get status mya:" + device_id + " " + str(e))
        print(datetime.datetime.now().time(), "Unable to get status mya:" + device_id + " " + str(e))

    return 0


def get_weather(weather_data):
    loop = asyncio.new_event_loop()

    try:
        # default to closed
        weather_data.alarm.main_garage = 1
        weather_data.alarm.mc_garage = 1

        asyncio.set_event_loop(loop)
        coroutine = async_get_myq(weather_data)
        loop.run_until_complete(coroutine)

    except Exception as e:
        logging.error("Unable to get myq:get_weather " + str(e))
        print(datetime.datetime.now().time(), "Unable to get myq:get_weather " + str(e))
    except:
        e = sys.exc_info()[0]
        logging.error("Unable to get myq:get_weather " + str(e))
        print(datetime.datetime.now().time(), "Unable to get myq:get_weather " + str(e))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
