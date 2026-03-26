import pytest
from ..src.weather.service import WeatherService
from ..src.weather.exceptions import CityNotFoundError

@pytest.fixture
def weather_service():
    return WeatherService()

def test_get_forecast_unknown_city(weather_service):
    with pytest.raises(CityNotFoundError):
        weather_service.get_forecast("paris")