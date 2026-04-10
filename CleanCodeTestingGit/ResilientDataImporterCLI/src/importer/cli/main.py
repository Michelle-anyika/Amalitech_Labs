import argparse

from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.repository.user_repository import UserRepository
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.services.importer_service import ImporterService


def main() -> None:
    """
    CLI entry point.
    """
    parser = argparse.ArgumentParser(
        description="Resilient Data Importer CLI"
    )
    parser.add_argument("file", help="Path to CSV file")

    args = parser.parse_args()

    repository = UserRepository("data/users.json")
    service = ImporterService(repository)

    service.import_data(args.file)


if __name__ == "__main__":
    main()