from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.exceptions.base import ImporterError


class DataValidationError(ImporterError):
    """
    Raised when user data fails validation checks.
    """

    def __init__(self, message: str = "Invalid data.") -> None:
        super().__init__(message)


class DuplicateUserError(ImporterError):
    """
    Raised when a duplicate user is detected.
    """

    def __init__(self, message: str = "Duplicate user detected.") -> None:
        super().__init__(message)