import unittest
from src.stations import sensorPush


class TestSensorPush(unittest.TestCase):

    # test get_weather raising exception
    @unittest.skip("Not implemented")
    def test_get_weather_exception(self):

        # Test exception
        with self.assertRaises(ValueError):
            sensorPush.get_weather("test")

    if __name__ == '__main__':
        unittest.main()


