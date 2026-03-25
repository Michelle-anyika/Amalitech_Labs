import pytest
import tempfile
import json
from pathlib import Path


@pytest.fixture
def temp_csv_file():
    content = "user_id,name,email\n1,John,john@example.com\n2,Jane,jane@example.com"
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as f:
        f.write(content)
        f.flush()
        yield f.name


@pytest.fixture
def invalid_csv_file():
    content = "user_id,name,email\n1,John,invalid-email"
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".csv") as f:
        f.write(content)
        f.flush()
        yield f.name


@pytest.fixture
def temp_json_file():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as f:
        json.dump([], f)
        f.flush()
        yield f.name