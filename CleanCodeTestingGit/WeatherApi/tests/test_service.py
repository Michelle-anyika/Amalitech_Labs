import pytest
from ..src.weather.service import WeatherService


@pytest.fixture
def weather_service():
    return WeatherService()


@pytest.mark.parametrize("city", ["Kigali", "Nairobi", "Lagos"])
def test_get_forecast_multiple_cities(weather_service, city):
    result = weather_service.get_forecast(city)

    assert result["city"] == city
    assert "temperature" in result
    assert "condition" in result