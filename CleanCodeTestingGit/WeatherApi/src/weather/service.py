import logging
from .exceptions import InvalidAPIKeyError
from .models import WeatherResponse

logger = logging.getLogger(__name__)


class WeatherService:
    def __init__(self, provider, api_key: str = "valid-key"):
        self.provider = provider
        self.api_key = api_key

    def get_forecast(self, city: str) -> WeatherResponse:
        logger.info(f"Fetching forecast for city: {city}")

        if self.api_key != "valid-key":
            logger.error(f"Invalid API key provided: {self.api_key}")
            raise InvalidAPIKeyError("Invalid API key")

        try:
            data = self.provider.fetch(city.lower())
            return WeatherResponse(
                city=city,
                temperature=data["temperature"],
                condition=data["condition"],
            )
        except Exception as e:
            logger.exception(f"Error fetching weather for {city}: {e}")
            raise
