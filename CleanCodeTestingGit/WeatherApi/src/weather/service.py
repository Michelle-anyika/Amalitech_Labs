# from .exceptions import CityNotFoundError
# import logging
from .exceptions import InvalidAPIKeyError

class WeatherService:
    def __init__(self, provider, api_key: str = "valid-key"):
        self.provider = provider
        self.api_key = api_key

    def get_forecast(self, city: str) -> dict:
        if self.api_key != "valid-key":
            raise InvalidAPIKeyError()

        data = self.provider.fetch(city.lower())

        return {"city": city, **data}