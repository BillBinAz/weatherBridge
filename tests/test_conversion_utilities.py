import unittest
from utilities import conversions as utilities


class TestUtilities(unittest.TestCase):

    def test_c_to_f(self):
        # Test 0C
        self.assertEqual(32.0, utilities.c_to_f(0))
        self.assertEqual(utilities.c_to_f(100), 212.0)
        # Test -40C
        self.assertEqual(utilities.c_to_f(-40), -40.0)
        # Test 37.7778C
        self.assertEqual(utilities.c_to_f(37.7778), 100.0)
        # Test 21.1111C
        self.assertEqual(utilities.c_to_f(21.1111), 70.0)

    def test_number_format_f(self):
        # Test 0
        self.assertEqual(utilities.format_f(0), 0)
        # Test 0.0
        self.assertEqual(utilities.format_f(0.0), 0.0)
        # Test 0.00
        self.assertEqual(utilities.format_f(0.00), 0.0)
        # Test 0.000
        self.assertEqual(utilities.format_f(0.000), 0.0)
        # Test 0.0000
        self.assertEqual(utilities.format_f(0.0000), 0.0)
        # Test 0.00000
        self.assertEqual(utilities.format_f(0.00000), 0.0)

    def test_c_to_f_exception(self):
        # Test exception
        with self.assertRaises(ValueError):
            utilities.c_to_f("test")

    def test_f_to_c(self):
        # Test 32F
        self.assertEqual(utilities.f_to_c(32), 0.0)
        # Test 212F
        self.assertEqual(utilities.f_to_c(212), 100.0)
        # Test -40F
        self.assertEqual(utilities.f_to_c(-40), -40.0)
        # Test 100F
        self.assertEqual(utilities.f_to_c(100), 37.8)
        # Test 70F
        self.assertEqual(utilities.f_to_c(70), 21.1)

    def test_f_to_c_exception(self):
        # Test exception
        with self.assertRaises(TypeError):
            utilities.f_to_c("test")

    # test compass direction deg_to_compass
    def test_deg_to_compass(self):
        # Test 0
        self.assertEqual(utilities.deg_to_compass(0).replace(" ", ""), "N")
        # Test 22.5
        self.assertEqual(utilities.deg_to_compass(22.5).replace(" ", ""), "NNE")
        # Test 45
        self.assertEqual(utilities.deg_to_compass(45).replace(" ", ""), "NE")
        # Test 67.5
        self.assertEqual(utilities.deg_to_compass(67.5).replace(" ", ""), "ENE")
        # Test 90
        self.assertEqual(utilities.deg_to_compass(90).replace(" ", ""), "E")
        # Test 112.5
        self.assertEqual(utilities.deg_to_compass(112.5).replace(" ", ""), "ESE")
        # Test 135
        self.assertEqual(utilities.deg_to_compass(135).replace(" ", ""), "SE")
        # Test 157.5
        self.assertEqual(utilities.deg_to_compass(157.5).replace(" ", ""), "SSE")
        # Test 180
        self.assertEqual(utilities.deg_to_compass(180).replace(" ", ""), "S")
        # Test 202.5
        self.assertEqual(utilities.deg_to_compass(202.5).replace(" ", ""), "SSW")
        # Test 225
        self.assertEqual(utilities.deg_to_compass(225).replace(" ", ""), "SW")
        # Test 247.5
        self.assertEqual(utilities.deg_to_compass(247.5).replace(" ", ""), "WSW")
        # Test 270
        self.assertEqual(utilities.deg_to_compass(270).replace(" ", ""), "W")
        # Test 292.5
        self.assertEqual(utilities.deg_to_compass(292.5).replace(" ", ""), "WNW")
        # Test 315
        self.assertEqual(utilities.deg_to_compass(315).replace(" ", ""), "NW")
        # Test 337.5
        self.assertEqual(utilities.deg_to_compass(337.5).replace(" ", ""), "NNW")
        # Test 360
        self.assertEqual(utilities.deg_to_compass(360).replace(" ", ""), "N")

    def test_deg_to_compass_exception(self):
        # Test exception
        with self.assertRaises(ValueError):
            utilities.deg_to_compass("test")

    def test_get_average(self):
        # test get_average(data, key)
        data = [
            {"temperature": 10},
            {"temperature": 20},
            {"temperature": 30}
        ]
        result = utilities.get_average(data, "temperature")
        self.assertEqual(result, 20.0)

    def test_get_average_empty(self):
        """Test get_average with empty list."""
        data = []
        result = utilities.get_average(data, "temperature")
        self.assertEqual(result, 0)

    def test_get_average_from_list(self):
        """Test get_average_from_list function."""
        data_list = ["10", "20", "30"]
        result = utilities.get_average_from_list(data_list)
        self.assertEqual(result, 20.0)

    def test_get_average_from_list_with_invalid(self):
        """Test get_average_from_list with invalid values."""
        data_list = ["10", "invalid", "30", "0.0"]
        result = utilities.get_average_from_list(data_list)
        # "invalid" and "0.0" are skipped, so average of 10 and 30 = 20.0
        self.assertEqual(result, 20.0)


if __name__ == '__main__':
    unittest.main()
