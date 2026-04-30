from abc import ABC, abstractmethod
from typing import List
from ..models.user import User


class ValidationServiceInterface(ABC):
    """
    Abstract Base Class for Validation Service.
    """

    @abstractmethod
    def validate(self, users: List[User]) -> List[User]:
        """
        Validates a list of users.
        """
        pass
