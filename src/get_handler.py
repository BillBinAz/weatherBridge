"""Weather Bridge REST API Handler

This module provides Flask endpoints to retrieve aggregated weather data
from multiple sources including Ecobee, Davis Weather Station, and SensorPush.
"""

from flask import Flask, jsonify
from weather import stations
import logging
import os

# Configure logging
log_file = os.environ.get('LOG_FILE', 'weather_bridge_rest.log')
logging.basicConfig(
    filename=log_file,
    format='%(asctime)s %(levelname)s {%(module)s} [%(funcName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/weather", methods=['GET'])
def get_weather():
    """
    Retrieve aggregated weather data from all configured sources.

    Returns:
        tuple: JSON response with weather data and HTTP status code
    """
    try:
        weather_data = stations.get_weather()
        logger.info("Weather data retrieved successfully")
        return weather_data.to_json(), 200, {'Content-Type': 'application/json; charset=utf-8'}
    except Exception as e:
        logger.error(f"Error retrieving weather data: {str(e)}")
        return jsonify({'error': 'Failed to retrieve weather data'}), 500


@app.route("/health", methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring and orchestration.

    Returns:
        tuple: JSON response indicating service health
    """
    return jsonify({'status': 'healthy'}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 8080)),
        debug=False
    )
