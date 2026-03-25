from importer.exceptions.base import ImporterError


class FileFormatError(ImporterError):
    """
    Raised when the input file format is invalid or malformed.
    """

    def __init__(self, message: str = "Invalid file format.") -> None:
        super().__init__(message)


class FileReadError(ImporterError):
    """
    Raised when a file cannot be read.
    """

    def __init__(self, message: str = "Error reading file.") -> None:
        super().__init__(message)


class FileNotFoundErrorCustom(ImporterError):
    """
    Raised when the specified file does not exist.
    """

    def __init__(self, message: str = "File not found.") -> None:
        super().__init__(message)