import unittest
from unittest.mock import patch, MagicMock
from weather import stations, data


class TestStations(unittest.TestCase):

    @patch('weather.stations.home_assistant.get_weather')
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_calls_all_stations(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that get_weather calls all station modules."""
        weather_data = stations.get_weather()

        self.assertIsInstance(weather_data, data.WeatherData)
        mock_home.assert_called_once_with(weather_data)
        mock_wifi.assert_called_once_with(weather_data)
        mock_sensor.assert_called_once_with(weather_data)
        mock_thermo.assert_called_once_with(weather_data)

    @patch('weather.stations.home_assistant.get_weather')
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_calculates_average_temp(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that average house temp is calculated correctly."""
        # Mock the station calls to set some temp values
        def set_temps(weather_data):
            weather_data.bedroom_left.temp = "70"
            weather_data.bedroom_right.temp = "72"
            weather_data.hallway_thermostat.sensor.temp = "71"
            weather_data.living_room.temp = "73"
            weather_data.master_bedroom.temp = "74"
            weather_data.office.temp = "69"

        mock_home.side_effect = set_temps
        mock_wifi.return_value = None
        mock_sensor.return_value = None
        mock_thermo.return_value = None

        result = stations.get_weather()

        # Average of [70,72,71,73,74,69] = 71.5
        self.assertEqual(result.whole_house_fan.houseTemp, 71.5)

    @patch('weather.stations.home_assistant.get_weather', side_effect=Exception("Test error"))
    @patch('weather.stations.wifiLogger.get_weather')
    @patch('weather.stations.sensorPush.get_weather')
    @patch('weather.stations.thermo_works.get_weather')
    def test_get_weather_handles_exceptions(self, mock_thermo, mock_sensor, mock_wifi, mock_home):
        """Test that get_weather handles exceptions gracefully."""
        with patch('weather.stations.logging.error') as mock_log:
            weather_data = stations.get_weather()

            self.assertIsInstance(weather_data, data.WeatherData)
            mock_log.assert_called()


if __name__ == '__main__':
    unittest.main()
