import pytest
from ..src.weather.service import WeatherService

@pytest.fixture
def weather_service():
    return WeatherService()


def test_get_forecast_unknown_city(weather_service):
    with pytest.raises(Exception):  # temporary
        weather_service.get_forecast("Paris")