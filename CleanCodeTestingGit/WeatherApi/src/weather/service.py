from .exceptions import InvalidAPIKeyError
from .models import WeatherResponse


class WeatherService:
    def __init__(self, provider, api_key: str = "valid-key"):
        self.provider = provider
        self.api_key = api_key

    def get_forecast(self, city: str) -> WeatherResponse:
        data = self.provider.fetch(city.lower())

        return WeatherResponse(
            city=city,
            temperature=data["temperature"],
            condition=data["condition"],
        )
