class WeatherService:
    def get_forecast(self, city: str) -> dict:
        forecasts = {
            "Kigali": {"temperature": 25, "condition": "Sunny"},
            "Nairobi": {"temperature": 22, "condition": "Cloudy"},
            "Lagos": {"temperature": 30, "condition": "Humid"},
        }

        if city not in forecasts:
            return None  # temporary (I’ll fix later)

        return {"city": city, **forecasts[city]}