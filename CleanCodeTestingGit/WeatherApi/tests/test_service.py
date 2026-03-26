import pytest
from ..src.weather.service import WeatherService
from ..src.weather.exceptions import CityNotFoundError
from ..src.weather.exceptions import InvalidAPIKeyError
@pytest.fixture
def weather_service():
    return WeatherService()

def test_get_forecast_unknown_city(weather_service):
    with pytest.raises(CityNotFoundError):
        weather_service.get_forecast("paris")


def test_invalid_api_key():
    service = WeatherService(api_key="bad-key")

    with pytest.raises(InvalidAPIKeyError):
        service.get_forecast("Kigali")

def test_service_uses_provider(mocker):
    mock_provider = mocker.Mock()
    mock_provider.fetch.return_value = {
        "temperature": 99,
        "condition": "Storm"
    }

    service = WeatherService(provider=mock_provider)

    result = service.get_forecast("Kigali")

    mock_provider.fetch.assert_called_once_with("kigali")
    assert result["temperature"] == 99