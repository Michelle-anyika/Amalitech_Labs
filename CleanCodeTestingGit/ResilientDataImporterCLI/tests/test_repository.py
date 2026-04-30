import pytest
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.models.user import User
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.repository.repo import UserRepository
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


def test_corrupt_json_file(tmp_path):
    file = tmp_path / "corrupt.json"
    file.write_text("{invalid_json: true}")

    repo = UserRepository(str(file))

    with pytest.raises(Exception):
        repo.load_users()

