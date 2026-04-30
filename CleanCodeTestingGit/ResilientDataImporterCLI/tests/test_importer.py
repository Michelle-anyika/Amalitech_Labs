from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.repository.repo import UserRepository
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.services.importer_service import ImporterService
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.services.validation_service import ValidationService


def test_full_import_flow(temp_csv_file, temp_json_file):
    repo = UserRepository(temp_json_file)
    validator = ValidationService()
    service = ImporterService(repo, validator)

    service.import_data(temp_csv_file)

    users = repo.load_users()

    assert len(users) == 2

def test_repository_mock(mocker):
    mock_repo = mocker.Mock()
    mock_validator = mocker.Mock()
    mock_repo.add_users.return_value = None

    service = ImporterService(mock_repo, mock_validator)

    mocker.patch("CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.services.importer_service.parse_csv", return_value=[
        {"user_id": "1", "name": "John", "email": "john@mail.com"}
    ])

    service.import_data("fake.csv")

    assert mock_repo.add_users.called