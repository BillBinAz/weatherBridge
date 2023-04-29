import pytest
import stations.isy994
ALARM_ZONES_CLOSED = '0'
ALARM_ZONES_OPEN = '1'


class TestISY994:

    # get zone status closed
    def test_get_zone_status_closed(self):
        # Test closed
        assert stations.isy994.get_zone_status(ALARM_ZONES_CLOSED) == 1

    # get zone status open
    def test_get_zone_status_open(self):
        # Test open
        assert stations.isy994.get_zone_status(ALARM_ZONES_OPEN) == 0

    # get zone status unknown
    def test_get_zone_status_unknown(self):
        # Test unknown
        assert stations.isy994.get_zone_status("unknown") == 0

    # get zone status exception
    def test_get_zone_status_exception(self):
        # ignore test
        pytest.skip("Not implemented")
        # Test exception
        with self.assertRaises(ValueError):
            stations.isy994.get_zone_status("test")






