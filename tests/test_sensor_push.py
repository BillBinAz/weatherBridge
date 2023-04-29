import pytest
import stations.sensorPush


class TestSensorPush:

    # test get_weather raising exception
    def test_get_weather_exception(self):
        pytest.skip("Not implemented")

        # Test exception
        with pytest.raises(Exception):
            stations.sensorPush.get_weather("test")




