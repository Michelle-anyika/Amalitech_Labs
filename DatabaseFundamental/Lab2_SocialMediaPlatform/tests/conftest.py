import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.postgres import PostgresPool
from src.db.postgres import get_connection, release_connection

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Ensure database schema is clean for tests."""
    pass
    # Depending on test strategy, we might wipe tables here.
    # For now, we will just use the pre-initialized DB.
    
@pytest.fixture(scope="function")
def db_conn():
    conn = get_connection()
    yield conn
    release_connection(conn)
