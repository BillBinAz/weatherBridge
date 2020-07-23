import sys
import logging
from flask import Flask
from rtl_433 import weather433
from weather import data

sys.path.append('../')
sys.path.append('./')

app = Flask(__name__)
logging.basicConfig(filename='/tmp/weather_bridge_rest_433.log', level=logging.INFO)


@app.route("/weather", methods=['GET'])
def get_weather():
    weather_data = data.WeatherData()
    weather_data = weather433.get_weather(weather_data)
    return weather_data.to_json(), 200, {'Content-Type': 'text/json; charset=utf-8'}
