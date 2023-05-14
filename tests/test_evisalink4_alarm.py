import unittest

import stations.evisalink4_alarm as evisalink4_alarm
from weather import data
from weather.data import WeatherData


class TestEvisalink4(unittest.TestCase):

    def test_station_data(self):
        http_return = evisalink4_alarm.get_html()
        self.assertIsNotNone(http_return)

    def test_parse_html(self):
        http_return = self.get_test_html()
        cur_weather: WeatherData = data.WeatherData()
        evisalink4_alarm.parse_html(cur_weather, http_return)
        evisalink4_alarm.determine_fan_status(cur_weather)

        self.assertEqual(cur_weather.alarm.all_zones_closed, 0)
        self.assertEqual(cur_weather.whole_house_fan.fan_zones_all, 1)
        self.assertEqual(cur_weather.whole_house_fan.fan_zones_some, 1)
        self.assertEqual(cur_weather.alarm.offices, 1)
        self.assertEqual(cur_weather.alarm.front_garage_door, 1)
        self.assertEqual(cur_weather.alarm.living_great, 0)
        self.assertEqual(cur_weather.alarm.master, 0)
        self.assertEqual(cur_weather.alarm.sliding_glass_door, 1)
        self.assertEqual(cur_weather.alarm.west_wing, 0)
        self.assertEqual(cur_weather.alarm.status, 0)
        self.assertEqual(cur_weather.alarm.status_label, "Not Ready")

    def test_get_weather_data(self):
        cur_weather = data.WeatherData()
        evisalink4_alarm.get_weather(cur_weather)

        self.assertLess(cur_weather.alarm.offices, 2)
        self.assertLess(cur_weather.alarm.front_garage_door, 2)
        self.assertLess(cur_weather.alarm.living_great, 2)
        self.assertLess(cur_weather.alarm.master, 2)
        self.assertLess(cur_weather.alarm.sliding_glass_door, 2)
        self.assertLess(cur_weather.alarm.west_wing, 2)

    def test_get_html(self):
        http_return = self.get_test_html()
        self.assertIsNotNone(http_return, None)

    @staticmethod
    def get_test_html():
        # read from resources folder
        with open("./resources/eve4.html", "r") as html_file:
            return html_file.read()


if __name__ == '__main__':
    unittest.main()