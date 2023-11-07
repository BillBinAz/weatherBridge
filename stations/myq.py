import asyncio
from aiohttp import ClientSession
import pymyq
import logging
import datetime
import sys
import Utilities.connect as connect

GAMBIT_MAIN_GARAGE = 'CG0846887725'
GAMBIT_MOTORCYCLE_GARAGE = 'CG0846887726'
SHOTGUN_DOUBLE_GARAGE = 'CG0850450103'
SHOTGUN_SINGLE_GARAGE = 'CG085045011E'
CONNECT_ITEM_ID = "7z57celfaxx275hrlue5wn6etu"


async def async_get_myq(weather_data) -> None:

    try:
        #
        # Get security data
        credentials = connect.get_credentials(CONNECT_ITEM_ID)
        user_name = credentials[0].value
        password = credentials[1].value

        async with ClientSession() as web_session:
            myq = await pymyq.login(user_name, password, web_session)
            devices = myq.covers

            # Shotgun Double Garage
            weather_data.alarm.double_garage = update(devices, SHOTGUN_DOUBLE_GARAGE)

            # Shotgun Single Garage
            weather_data.alarm.single_garage = update(devices, SHOTGUN_SINGLE_GARAGE)

            # Motorcycle Garage
            weather_data.alarm.mc_garage = update(devices, GAMBIT_MOTORCYCLE_GARAGE)

            # Main Garage
            weather_data.alarm.main_garage = update(devices, GAMBIT_MAIN_GARAGE)

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
