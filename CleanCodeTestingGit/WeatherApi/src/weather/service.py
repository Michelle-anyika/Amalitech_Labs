class WeatherService:
    def get_forecast(self, city: str) -> dict:
        data = {
            "Kigali": {"temperature": 25, "condition": "Sunny"},
            "Nairobi": {"temperature": 22, "condition": "Cloudy"},
            "Lagos": {"temperature": 30, "condition": "Humid"},
        }

        if city in data:
            return {
                "city": city,
                **data[city],
            }