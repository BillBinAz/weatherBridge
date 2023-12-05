import unittest
from unittest import mock
import xml.etree.ElementTree
from stations import airScape


XML_DIRTY = """<?xml version="1.0" encoding="UTF-8"?> 
                    <airscapewhf>
                        <server_response>��$�޻@j2a�e0������|�</server_response>
                    </airscapewhf>"""
XML_CLEAN = """<?xml version="1.0" encoding="UTF-8"?><airscapewhf></airscapewhf>"""


class TestAirScape(unittest.TestCase):

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

    # Test get_node_xml function
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get_node_xml(self, mock_post):

        clean_node = airScape.get_node_xml()
        test_node = xml.etree.ElementTree.fromstring(XML_CLEAN)

        # Test get_node_xml
        self.assertEqual(test_node.tag, clean_node.tag)

    # Test clean_up_xml function
    def test_clean_up_xml(self):

        # Test clean_up_xml
        cleaned_xml = airScape.clean_up_xml(XML_DIRTY.encode("utf=8", "ignore"))\
            .replace("\n", "")\
            .replace("\t", "")

        self.assertEqual(XML_CLEAN.replace(" ", ""), cleaned_xml.replace(" ", ""))

    if __name__ == '__main__':
        unittest.main()