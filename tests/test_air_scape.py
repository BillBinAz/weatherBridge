import unittest
from unittest import mock
import stations.airScape
import xml.etree.ElementTree

XML_DIRTY = """<?xml version="1.0" encoding="UTF-8"?> 
                    <airscapewhf> 
                        <server_response>��$�޻@j2a�e0������|�</server_response>
                    </airscapewhf>"""
XML_CLEAN = """<?xml version="1.0" encoding="UTF-8"?></airscapewhf>"""


class TestAirScape(unittest.TestCase):

    if __name__ == '__main__':
        unittest.main()

    # This method will be used by the mock to replace requests.get
    def mocked_requests_post(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
                self.content = XML_DIRTY.encode("utf=8", "ignore")

            def close(self):
                return

            def json(self):
                return self.json_data

        if args[0] == "http://fan.evilminions.org/status.xml.cgi":
            return MockResponse(XML_DIRTY, 200)

        return MockResponse(None, 404)

    # Test celcius to farenheit conversion
    def test_c_to_f(self):
        # Test 0C
        assert stations.airScape.c_to_f(0) == 32.0
        # Test 100C
        assert stations.airScape.c_to_f(100) == 212.0
        # Test -40C
        assert stations.airScape.c_to_f(-40) == -40.0
        # Test 37.7778C
        assert stations.airScape.c_to_f(37.7778) == 100.0
        # Test 21.1111C
        assert stations.airScape.c_to_f(21.1111) == 70.0

    def test_c_to_f_exception(self):
        # Test exception
        with unittest.TestCase.assertRaises(self, ValueError):
            stations.airScape.c_to_f("test")

    # test formatting to 2 decimal places
    def test_number_format_f(self):
        # Test 0
        assert stations.airScape.format_f(0, "test") == 0
        # Test 0.0
        assert stations.airScape.format_f(0.0, "test") == 0.0
        # Test 0.00
        assert stations.airScape.format_f(0.00, "test") == 0.0
        # Test 0.000
        assert stations.airScape.format_f(0.000, "test") == 0.0
        # Test 0.0000
        assert stations.airScape.format_f(0.0000, "test") == 0.0
        # Test 0.00000
        assert stations.airScape.format_f(0.00000, "test") == 0.0

    # Test get_node_xml function
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @unittest.skip("Not implemented")
    def test_get_node_xml(self, mock_post):

        # Test get_node_xml
        self.assertEqual(stations.airScape.get_node_xml(), XML_CLEAN)

    # Test clean_up_xml function
    @unittest.skip("Not implemented")
    def test_clean_up_xml(self):

        self.assertEqual(stations.airScape.clean_up_xml(XML_DIRTY.encode("utf=8", "ignore")), XML_CLEAN)
