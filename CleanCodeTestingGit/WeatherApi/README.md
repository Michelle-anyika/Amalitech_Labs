# Weather API Service

A simple weather forecast service built with TDD principles, showcasing Dependency Injection and interface-based design.

## Features
- Fetch weather forecasts for supported cities.
- API Key validation.
- Mock weather provider for testing.
- Comprehensive logging.

## Supported Cities
- Kigali
- Nairobi
- Lagos

## How to Run Tests
To run the tests, ensure you have `pytest` installed and run:
```bash
pytest
```
To run with coverage:
```bash
pytest --cov=src
```

## Exceptions
The service raises the following custom exceptions:
- `InvalidAPIKeyError`: Raised when an incorrect API key is provided to the service.
- `CityNotFoundError`: Raised when a city is requested that the provider does not have data for.
