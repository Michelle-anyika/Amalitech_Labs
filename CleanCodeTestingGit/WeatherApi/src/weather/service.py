class WeatherService:
    def get_forecast(self, city: str):
        if city == "Kigali":
            return {
                "city": "Kigali",
                "temperature": 25,
                "condition": "Sunny",
            }