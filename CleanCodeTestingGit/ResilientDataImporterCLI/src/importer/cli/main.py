import argparse
from pathlib import Path
from ..repository.repo import UserRepository
from ..services.importer_service import ImporterService


def main() -> None:
    parser = argparse.ArgumentParser(description="Resilient Data Importer CLI")
    parser.add_argument("file", help="Path to CSV file")
    parser.add_argument("--db", default="data/users.json", help="Path to JSON DB")

    args = parser.parse_args()

    # Resolve paths relative to project root
    project_root = Path(__file__).parents[2]  # src/importer/cli -> go up 2 levels to src
    csv_path = (project_root / args.file).resolve()
    db_path = (project_root / args.db).resolve()

    repository = UserRepository(str(db_path))
    service = ImporterService(repository)

    service.import_data(str(csv_path))


if __name__ == "__main__":
    main()
