from dataclasses import dataclass


@dataclass
class User:
    """
    Represents a user entity.

    Attributes:
        user_id (str): Unique identifier for the user.
        name (str): Full name of the user.
        email (str): Email address of the user.
    """

    user_id: str
    name: str
    email: str