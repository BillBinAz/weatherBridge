import unittest
import stations.evisalink4_alarm as evisalink4_alarm
from weather import stations, data


class TestEvisalink4(unittest.TestCase):

    def test_station_data(self):
        http_return = evisalink4_alarm.get_html()
        self.assertIsNotNone(http_return)

    def test_parse_zone_info(self):
        http_return = self.get_test_html()
        cur_weather = data.WeatherData()
        evisalink4_alarm.parse_zone_info(cur_weather, http_return)

        self.assertEqual(cur_weather.alarm.offices, 0)
        self.assertEqual(cur_weather.alarm.front_garage_door, 1)
        self.assertEqual(cur_weather.alarm.living_great, 1)
        self.assertEqual(cur_weather.alarm.master, 1)
        self.assertEqual(cur_weather.alarm.sliding_glass_door, 1)
        self.assertEqual(cur_weather.alarm.west_wing, 1)

    def test_get_weather_data(self):
        cur_weather = data.WeatherData()
        evisalink4_alarm.get_weather(cur_weather)

        self.assertLess(cur_weather.alarm.offices, 2)
        self.assertLess(cur_weather.alarm.front_garage_door, )
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