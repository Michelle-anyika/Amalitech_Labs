import psycopg2
from psycopg2 import pool
import logging
from src.config.settings import (
    POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT
)

logger = logging.getLogger(__name__)

class PostgresPool:
    _pool = None

    @classmethod
    def get_pool(cls):
        if cls._pool is None:
            try:
                cls._pool = psycopg2.pool.SimpleConnectionPool(
                    1, 20,
                    database=POSTGRES_DB,
                    user=POSTGRES_USER,
                    password=POSTGRES_PASSWORD,
                    host=POSTGRES_HOST,
                    port=POSTGRES_PORT
                )
            except Exception as e:
                logger.error(f"Error connecting to PostgreSQL: {e}")
                raise e
        return cls._pool

    @classmethod
    def close_pool(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None

def get_connection():
    pool = PostgresPool.get_pool()
    return pool.getconn()

def release_connection(conn):
    pool = PostgresPool.get_pool()
    pool.putconn(conn)
