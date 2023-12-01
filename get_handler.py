from flask import Flask
from weather import stations
import logging
import sys

sys.path.append('/home/admin/.local/usr/bin')

app = Flask(__name__)
logging.basicConfig(filename='/var/log/weather_bridge_rest.log',
                    format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d,%H:%M:%S', level=logging.INFO)


@app.route("/weather", methods=['GET'])
def get_weather():
    weather_data = stations.get_weather()
    return weather_data.to_json(), 200, {'Content-Type': 'text/json; charset=utf-8'}


# if __name__ == "__main__":
#    app.debug = False
#    port = int(os.environ.get('PORT', 8080))
#    waitress.serve(app, port=port)
