class CityNotFoundError(Exception):
    """Raised when the requested city is not available."""
    pass

class InvalidAPIKeyError(Exception):
    """Raised when the API key is invalid."""
    pass