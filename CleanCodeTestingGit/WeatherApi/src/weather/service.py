from .exceptions import CityNotFoundError
import logging
from .exceptions import InvalidAPIKeyError

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, api_key: str = "valid-key"):
        self.api_key = api_key

    def get_forecast(self, city: str) -> dict:
        logger.info(f"Fetching weather for {city}")

        if self.api_key != "valid-key":
            raise InvalidAPIKeyError("Invalid API key")

        forecasts = {
            "kigali": {"temperature": 25, "condition": "Sunny"},
            "nairobi": {"temperature": 22, "condition": "Cloudy"},
            "lagos": {"temperature": 30, "condition": "Humid"},
        }

        city_key = city.lower()  # normalize input

        if city_key not in forecasts:
            raise CityNotFoundError(f"{city} not found")

        return {
            "city": city,
            **forecasts[city_key],
        }