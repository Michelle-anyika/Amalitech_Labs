import pytest
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.models.user import User
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.repository.user_repository import UserRepository
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.exceptions.data_exceptions import DuplicateUserError


def test_add_users_success(temp_json_file):
    repo = UserRepository(temp_json_file)

    users = [User("1", "John", "john@mail.com")]

    repo.add_users(users)

    saved_users = repo.load_users()
    assert len(saved_users) == 1


def test_duplicate_user(temp_json_file):
    repo = UserRepository(temp_json_file)

    user = User("1", "John", "john@mail.com")

    repo.add_users([user])

    with pytest.raises(DuplicateUserError):
        repo.add_users([user])

