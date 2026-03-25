import csv
from typing import List, Dict

from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.exceptions.file_exceptions import (
    FileNotFoundErrorCustom,
    FileFormatError,
    FileReadError,
)
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.utils.file_manager import FileManager


def parse_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Parses a CSV file and returns a list of dictionaries.

    Args:
        file_path (str): Path to CSV file.

    Returns:
        List[Dict[str, str]]: Parsed user data.

    Raises:
        FileNotFoundErrorCustom: If file does not exist.
        FileFormatError: If CSV format is invalid.
        FileReadError: If file cannot be read.
    """
    try:
        with FileManager(file_path, "r") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                raise FileFormatError("CSV file has no headers.")

            data = [row for row in reader]

            return data

    except FileNotFoundError:
        raise FileNotFoundErrorCustom(f"File '{file_path}' not found.")

    except csv.Error as e:
        raise FileFormatError(f"CSV parsing error: {e}")

    except Exception as e:
        raise FileReadError(f"Unexpected error: {e}")