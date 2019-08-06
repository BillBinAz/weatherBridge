import sys
sys.path.append('/home/admin/.local/usr/bin')

from flask import Flask
from weather import stations
app = Flask(__name__)

@app.route("/")
def system_check():
	return "System Up"

@app.route("/weather")
def get_weather():
	weather_data = stations.get_weather()
	return weather_data.to_json(), 200, {'Content-Type': 'text/json; charset=utf-8'}

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
