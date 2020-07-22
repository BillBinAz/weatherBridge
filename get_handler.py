from flask import Flask
from weather import stations
import sys
sys.path.append('/home/admin/.local/usr/bin')

app = Flask(__name__)


@app.route("/weather", methods=['GET'])
def get_weather():
	weather_data = stations.get_weather()
	print("got weather data")
	return weather_data.to_json(), 200, {'Content-Type': 'text/json; charset=utf-8'}

