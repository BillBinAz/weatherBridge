from flask import Flask
from weather import stations
import sys
sys.path.append('/home/admin/.local/usr/bin')

app = Flask(__name__)


@app.route("/weather", methods=['GET'])
def get_weather():
	weather_data = stations.get_weather()
	return weather_data.to_json()


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8080)
