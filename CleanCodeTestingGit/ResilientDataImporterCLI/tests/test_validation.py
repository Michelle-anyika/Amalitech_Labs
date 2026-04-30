import pytest
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.models.user import User
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.services.validation_service import ValidationService
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.exceptions.data_exceptions import DataValidationError


def test_valid_users():
    service = ValidationService()
    users = [User("1", "John", "john@mail.com")]

    result = service.validate(users)

    assert len(result) == 1


def test_invalid_email():
    service = ValidationService()
    users = [User("1", "John", "invalid-email")]

    with pytest.raises(DataValidationError):
        service.validate(users)


def test_missing_fields():
    service = ValidationService()
    users = [User("", "John", "john@mail.com")]

    with pytest.raises(DataValidationError):
        service.validate(users)


def test_empty_user_list():
    service = ValidationService()
    assert service.validate([]) == []


def test_validation_fails_on_first_error():
    service = ValidationService()
    users = [
        User("1", "John", "john@mail.com"),
        User("2", "Jane", "invalid-email"),
    ]

    with pytest.raises(DataValidationError, match="Invalid email"):
        service.validate(users)