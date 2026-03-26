import pytest
from ..src.weather.service import WeatherService


def test_get_forecast_valid_city():
    service = WeatherService()

    result = service.get_forecast("Kigali")

    assert result["city"] == "Kigali"
    assert "temperature" in result
    assert "condition" in result