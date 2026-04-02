import re
from typing import List

from ..models.user import User
from ..exceptions.data_exceptions import DataValidationError


class ValidationService:
    """
    Handles validation of user data.
    """

    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    def validate(self, users: List[User]) -> List[User]:
        """
        Validates a list of users.

        Args:
            users (List[User]): List of users to validate.

        Returns:
            List[User]: Validated users.

        Raises:
            DataValidationError: If validation fails.
        """
        validated_users: List[User] = []

        for user in users:
            if not user.user_id or not user.name or not user.email:
                raise DataValidationError("Missing required user fields.")

            if not re.match(self.EMAIL_REGEX, user.email):
                raise DataValidationError(f"Invalid email: {user.email}")

            validated_users.append(user)

        return validated_users