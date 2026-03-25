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