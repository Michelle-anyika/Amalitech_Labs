from ..src.weather.service import WeatherService

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