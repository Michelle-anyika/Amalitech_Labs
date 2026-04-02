class ImporterError(Exception):
    """
    Base exception class for all importer-related errors.

    This class serves as the root of the custom exception hierarchy
    for the Resilient Data Importer CLI.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)