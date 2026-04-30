from abc import ABC, abstractmethod
from typing import List
from ..models.user import User


class UserRepositoryInterface(ABC):
    """
    Abstract Base Class for User Repository.
    """

    @abstractmethod
    def load_users(self) -> List[User]:
        """
        Loads users from storage.
        """
        pass

    @abstractmethod
    def save_users(self, users: List[User]) -> None:
        """
        Saves users to storage.
        """
        pass

    @abstractmethod
    def add_users(self, new_users: List[User]) -> None:
        """
        Adds new users.
        """
        pass
