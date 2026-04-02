from typing import List

from ..models.user import User
from ..parser.csv_parser import parse_csv
from ..services.validation_service import ValidationService
from ..repository.repo import UserRepository
from ..utils.logger import setup_logger


class ImporterService:
    """
    Orchestrates the import process.
    """

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        self.validator = ValidationService()
        self.logger = setup_logger()

    def import_data(self, file_path: str) -> None:
        """
        Imports user data from CSV into JSON storage.

        Args:
            file_path (str): Path to CSV file.
        """
        try:
            self.logger.info("Starting import process...")

            raw_data = parse_csv(file_path)

            users: List[User] = [
                User(
                    user_id=row["user_id"],
                    name=row["name"],
                    email=row["email"],
                )
                for row in raw_data
            ]

            validated_users = self.validator.validate(users)

            self.repository.add_users(validated_users)

            self.logger.info("Import completed successfully.")

        except Exception as e:
            self.logger.error(f"Import failed: {e}")
            raise