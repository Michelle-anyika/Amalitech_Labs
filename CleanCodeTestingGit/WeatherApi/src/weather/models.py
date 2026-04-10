from dataclasses import dataclass


@dataclass
class WeatherResponse:
    city: str
    temperature: int
    condition: str
