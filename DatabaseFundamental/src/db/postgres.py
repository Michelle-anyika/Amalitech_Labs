"""
PostgreSQL database connection and pooling management
"""
import psycopg2
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import logging
from typing import Optional, Dict, Any, List

from src.config.settings import settings

logger = logging.getLogger(__name__)


class PostgreSQLPool:
    """Manages PostgreSQL connection pooling"""

    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgreSQLPool, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._pool is None:
            self._init_pool()

    def _init_pool(self):
        """Initialize the connection pool"""
        try:
            self._pool = psycopg2.pool.SimpleConnectionPool(
                minconn=settings.POSTGRES_POOL_MIN_SIZE,
                maxconn=settings.POSTGRES_POOL_MAX_SIZE,
                host=settings.POSTGRES_HOST,
                port=settings.POSTGRES_PORT,
                database=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD
            )
            logger.info("PostgreSQL connection pool initialized successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(f"Error initializing database pool: {error}")
            raise

    @contextmanager
    def get_connection(self):
        """
        Context manager for getting a connection from the pool

        Yields:
            psycopg2.connection: A database connection
        """
        connection = self._pool.getconn()
        try:
            yield connection
        finally:
            self._pool.putconn(connection)

    def close_all_connections(self):
        """Close all connections in the pool"""
        if self._pool:
            self._pool.closeall()
            self._pool = None
            logger.info("All connections closed")


class PostgreSQLClient:
    """Client for PostgreSQL database operations"""

    def __init__(self):
        self.pool = PostgreSQLPool()

    def execute_query(
        self,
        query: str,
        params: Optional[tuple] = None,
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> Optional[Any]:
        """
        Execute a SELECT query

        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)
            fetch_one: Fetch only one result
            fetch_all: Fetch all results

        Returns:
            Query results or None
        """
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)

                    if fetch_one:
                        return cursor.fetchone()
                    elif fetch_all:
                        return cursor.fetchall()
                    else:
                        return None
        except Exception as error:
            logger.error(f"Error executing query: {error}")
            raise

    def execute_update(
        self,
        query: str,
        params: Optional[tuple] = None
    ) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE query

        Args:
            query: SQL query string
            params: Query parameters (for parameterized queries)

        Returns:
            Number of affected rows
        """
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    connection.commit()
                    rows_affected = cursor.rowcount
                    logger.info(f"Query executed. Rows affected: {rows_affected}")
                    return rows_affected
        except Exception as error:
            logger.error(f"Error executing update: {error}")
            raise

    def execute_transaction(self, operations: List[tuple]) -> bool:
        """
        Execute multiple operations in a transaction

        Args:
            operations: List of (query, params) tuples

        Returns:
            True if transaction succeeded
        """
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    for query, params in operations:
                        cursor.execute(query, params)
                    connection.commit()
                    logger.info("Transaction executed successfully")
                    return True
        except Exception as error:
            logger.error(f"Error executing transaction: {error}")
            with self.pool.get_connection() as connection:
                connection.rollback()
            raise

    def call_procedure(
        self,
        procedure_name: str,
        params: Optional[tuple] = None
    ) -> Optional[Any]:
        """
        Call a stored procedure

        Args:
            procedure_name: Name of the procedure
            params: Procedure parameters

        Returns:
            Procedure results
        """
        try:
            with self.pool.get_connection() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.callproc(procedure_name, params)
                    connection.commit()
                    return cursor.fetchall()
        except Exception as error:
            logger.error(f"Error calling procedure: {error}")
            raise

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists in the database"""
        query = """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = %s
            );
        """
        result = self.execute_query(query, (table_name,), fetch_one=True)
        return result['exists'] if result else False

    def close(self):
        """Close all database connections"""
        self.pool.close_all_connections()


# Singleton instance
postgres_client = PostgreSQLClient()

