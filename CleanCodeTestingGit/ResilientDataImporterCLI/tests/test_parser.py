import pytest
from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.parser.csv_parser import parse_csv


@pytest.mark.parametrize(
    "content,expected_count",
    [
        ("user_id,name,email\n1,A,a@mail.com", 1),
        ("user_id,name,email\n1,A,a@mail.com\n2,B,b@mail.com", 2),
    ],
)
def test_parse_valid_csv(tmp_path, content, expected_count):
    file = tmp_path / "test.csv"
    file.write_text(content)

    result = parse_csv(str(file))

    assert len(result) == expected_count


def test_parse_missing_file():
    with pytest.raises(Exception):
        parse_csv("non_existent.csv")


def test_parse_empty_csv(tmp_path):
    file = tmp_path / "empty.csv"
    file.write_text("user_id,name,email\n")

    result = parse_csv(str(file))
    assert len(result) == 0


from CleanCodeTestingGit.ResilientDataImporterCLI.src.importer.exceptions.file_exceptions import FileFormatError


def test_parse_corrupt_csv(tmp_path):
    file = tmp_path / "corrupt.csv"
    file.write_text("user_id,name\n1,A")  # Missing email column

    with pytest.raises(FileFormatError):
        parse_csv(str(file))