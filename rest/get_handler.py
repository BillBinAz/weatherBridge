from flask import Flask

import weather.data
import weather.stations

app = Flask(__name__)


@app.route("/")
def sytem_check():
	return "System Up"


@app.route("/weather")
def get_weather():
	data = weather.stations.get_weather_data()
	return Flask.jsonify(data)


if __name__ == "__main__":
	app.run()
