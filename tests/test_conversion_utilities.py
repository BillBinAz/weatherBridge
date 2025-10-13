import unittest
from utilities import conversions as utilities


class TestUtilities(unittest.TestCase):

    def test_c_to_f(self):
        # Test 0C
        self.assertEqual(32.0, utilities.c_to_f(0))
        assert utilities.c_to_f(100) == 212.0
        # Test -40C
        assert utilities.c_to_f(-40) == -40.0
        # Test 37.7778C
        assert utilities.c_to_f(37.7778) == 100.0
        # Test 21.1111C
        assert utilities.c_to_f(21.1111) == 70.0

    def test_number_format_f(self):
        # Test 0
        assert utilities.format_f(0) == 0
        # Test 0.0
        assert utilities.format_f(0.0) == 0.0
        # Test 0.00
        assert utilities.format_f(0.00) == 0.0
        # Test 0.000
        assert utilities.format_f(0.000) == 0.0
        # Test 0.0000
        assert utilities.format_f(0.0000) == 0.0
        # Test 0.00000
        assert utilities.format_f(0.00000) == 0.0

    def test_c_to_f_exception(self):
        # Test exception
        with unittest.TestCase.assertRaises(self, ValueError):
            utilities.c_to_f("test")

    def test_f_to_c(self):
        # Test 32F
        assert utilities.f_to_c(32) == 0.0
        # Test 212F
        assert utilities.f_to_c(212) == 100.0
        # Test -40F
        assert utilities.f_to_c(-40) == -40.0
        # Test 100F
        assert utilities.f_to_c(100) == 37.8
        # Test 70F
        assert utilities.f_to_c(70) == 21.1

    def test_f_to_c_exception(self):
        # Test exception
        with unittest.TestCase.assertRaises(self, TypeError):
            utilities.f_to_c("test")

    # test compass direction deg_to_compass
    def test_deg_to_compass(self):
        # Test 0
        assert utilities.deg_to_compass(0).replace(" ", "") == "N"
        # Test 22.5
        assert utilities.deg_to_compass(22.5).replace(" ", "") == "NNE"
        # Test 45
        assert utilities.deg_to_compass(45).replace(" ", "") == "NE"
        # Test 67.5
        assert utilities.deg_to_compass(67.5).replace(" ", "") == "ENE"
        # Test 90
        assert utilities.deg_to_compass(90).replace(" ", "") == "E"
        # Test 112.5
        assert utilities.deg_to_compass(112.5).replace(" ", "") == "ESE"
        # Test 135
        assert utilities.deg_to_compass(135).replace(" ", "") == "SE"
        # Test 157.5
        assert utilities.deg_to_compass(157.5).replace(" ", "") == "SSE"
        # Test 180
        assert utilities.deg_to_compass(180).replace(" ", "") == "S"
        # Test 202.5
        assert utilities.deg_to_compass(202.5).replace(" ", "") == "SSW"
        # Test 225
        assert utilities.deg_to_compass(225).replace(" ", "") == "SW"
        # Test 247.5
        assert utilities.deg_to_compass(247.5).replace(" ", "") == "WSW"
        # Test 270
        assert utilities.deg_to_compass(270).replace(" ", "") == "W"
        # Test 292.5
        assert utilities.deg_to_compass(292.5).replace(" ", "") == "WNW"
        # Test 315
        assert utilities.deg_to_compass(315).replace(" ", "") == "NW"
        # Test 337.5
        assert utilities.deg_to_compass(337.5).replace(" ", "") == "NNW"
        # Test 360
        assert utilities.deg_to_compass(360).replace(" ", "") == "N"

    def test_deg_to_compass_exception(self):
        # Test exception
        with unittest.TestCase.assertRaises(self, ValueError):
            utilities.deg_to_compass("test")

    @unittest.skip("Not implemented")
    def test_get_average(self):
        # test get_average(data, key)
        data = [0, 1, 2, 3, 4, 5]
        key = 0
        assert utilities.get_average(data, key) == 2.5
        key = 1
        assert utilities.get_average(data, key) == 3.5
        key = 2
        assert utilities.get_average(data, key) == 4.5
        key = 3
        assert utilities.get_average(data, key) == 5.5
        key = 4
        assert utilities.get_average(data, key) == 6.5
        key = 5
        assert utilities.get_average(data, key) == 7.5
        key = 6
        assert utilities.get_average(data, key) == 0.0


if __name__ == '__main__':
    unittest.main()
