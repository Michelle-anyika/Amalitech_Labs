from ..src.weather.service import WeatherService
from ..src.weather.provider import MockWeatherProvider
from ..src.weather.exceptions import InvalidAPIKeyError
from ..src.weather.exceptions import CityNotFoundError

import pytest


def test_service_uses_provider(mocker):
    mock_provider = mocker.Mock()
    mock_provider.fetch.return_value = {"temperature": 99, "condition": "Storm"}

    service = WeatherService(provider=mock_provider)

    result = service.get_forecast("Kigali")

    mock_provider.fetch.assert_called_once_with("kigali")
    assert result.temperature == 99
    assert result.city == "Kigali"


def test_mock_provider_valid_city():
    provider = MockWeatherProvider()

    result = provider.fetch("kigali")

    assert result.temperature == 25


def test_invalid_api_key(weather_service):
    service = WeatherService(provider=MockWeatherProvider(), api_key="bad")

    with pytest.raises(InvalidAPIKeyError):
        service.get_forecast("Kigali")


@pytest.mark.parametrize("city", ["Paris", "London"])
def test_unknown_cities(city):
    service = WeatherService(provider=MockWeatherProvider())

    with pytest.raises(CityNotFoundError):
        service.get_forecast(city)
