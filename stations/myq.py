import asyncio
from aiohttp import ClientSession
import pymyq
import logging
import datetime

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

            # Return only cover devices:
            devices = myq.covers

            # Bike Garage
            garage = devices[BIKE_GARAGE]
            online = garage.online
            state = garage.state
            name = garage.name

            if online and state == 'closed':
                weather_data.alarm.bike_garage = 1
            else:
                weather_data.alarm.bike_garage = 0

            # Motorcycle Garage
            garage = devices[MOTORCYCLE_GARAGE]
            online = garage.online
            state = garage.state
            name = garage.name

            if online and state == 'closed':
                weather_data.alarm.mc_garage = 1
            else:
                weather_data.alarm.mc_garage = 0

            # Main Garage
            garage = devices[MAIN_GARAGE]
            online = garage.online
            state = garage.state
            name = garage.name

            if online and state == 'closed':
                weather_data.alarm.main_garage = 1
            else:
                weather_data.alarm.main_garage = 0

    except Exception as e:
        logging.error( "Unable to retrieve myq.covers " + str(e))
        print(datetime.datetime.now().time(), "Unable to retrieve myq.covers " + str(e))
    return


def get_weather(weather_data):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coroutine = async_get_myq(weather_data)
        loop.run_until_complete(coroutine)
    except Exception as e:
        logging.error("MyQ: get_weather " + str(e))
        print(datetime.datetime.now().time(), "MyQ: get_weather  " + str(e))
    return
