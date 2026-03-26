from abc import ABC, abstractmethod
from .exceptions import CityNotFoundError


class WeatherProvider(ABC):

    @abstractmethod
    def fetch(self, city: str) -> dict:
        pass


class MockWeatherProvider(WeatherProvider):
    def fetch(self, city: str) -> dict:
        data = {
            "kigali": {"temperature": 25, "condition": "Sunny"},
            "nairobi": {"temperature": 22, "condition": "Cloudy"},
            "lagos": {"temperature": 30, "condition": "Humid"},
        }

        if city not in data:
            raise CityNotFoundError()

        return data[city]
