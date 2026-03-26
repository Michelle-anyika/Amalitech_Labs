class WeatherService:
    def get_forecast(self, city: str) -> dict:
        if city == "Kigali":
            return {
                "city": "Kigali",
                "temperature": 25,
                "condition": "Sunny",
            }