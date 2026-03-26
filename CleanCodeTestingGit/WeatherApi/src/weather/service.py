class WeatherService:
    def get_forecast(self, city: str) -> dict:
        forecasts = {
            "Kigali": {"temperature": 25, "condition": "Sunny"},
            "Nairobi": {"temperature": 22, "condition": "Cloudy"},
            "Lagos": {"temperature": 30, "condition": "Humid"},
        }

        if city not in forecasts:
            raise Exception("City not found")

        return {"city": city, **forecasts[city]}