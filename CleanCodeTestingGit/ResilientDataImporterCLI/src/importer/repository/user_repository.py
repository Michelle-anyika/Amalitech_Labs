import json
from typing import List

from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.models.user import User
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.exceptions.data_exceptions import DuplicateUserError
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.utils.file_manager import FileManager


class UserRepository:
    """
    Handles storage and retrieval of users in a JSON file.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def load_users(self) -> List[User]:
        """
        Loads users from the JSON file.

        Returns:
            List[User]: List of users.
        """
        try:
            with FileManager(self.file_path, "r") as file:
                data = json.load(file)
                return [User(**user) for user in data]
        except FileNotFoundError:
            return []

    def save_users(self, users: List[User]) -> None:
        """
        Saves users to the JSON file.

        Args:
            users (List[User]): Users to save.
        """
        with FileManager(self.file_path, "w") as file:
            json.dump([user.__dict__ for user in users], file, indent=4)

    def add_users(self, new_users: List[User]) -> None:
        """
        Adds new users, preventing duplicates.

        Args:
            new_users (List[User]): Users to add.

        Raises:
            DuplicateUserError: If duplicate user_id found.
        """
        existing_users = self.load_users()
        existing_ids = {user.user_id for user in existing_users}

        for user in new_users:
            if user.user_id in existing_ids:
                raise DuplicateUserError(
                    f"User with ID {user.user_id} already exists."
                )

        updated_users = existing_users + new_users
        self.save_users(updated_users)