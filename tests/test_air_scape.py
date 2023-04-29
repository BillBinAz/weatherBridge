import pytest
import stations.airScape


class TestAirScape:

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
        with pytest.raises(ValueError):
            stations.airScape.c_to_f("test")

    # test formatting to 2 decimal places
    def test_format_f(self):
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
    def test_get_node_xml(self):
        pytest.skip("Not implemented")

    # Test clean_up_xml function
    def test_clean_up_xml(self):
        pytest.skip("Not implemented")
        # Test xml_data removed server_response
        xml_dirty_data = """<?xml version="1.0" encoding="UTF-8"?> 
                    <airscapewhf> 
                        <server_response>��$�޻@j2a�e0������|�</server_response>
                    </airscapewhf>"""
        xml_clean_data = """<?xml version="1.0" encoding="UTF-8"?> 
                    <airscapewhf>
                        <server_response></server_response>
                    </airscapewhf>"""

        assert stations.airScape.clean_up_xml(xml_dirty_data) == xml_clean_data


