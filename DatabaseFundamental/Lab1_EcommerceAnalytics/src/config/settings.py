"""
Configuration management for the e-commerce data pipeline
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""

    # PostgreSQL
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce_db")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "ecommerce_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ecommerce_password")
    POSTGRES_POOL_MIN_SIZE = int(os.getenv("POSTGRES_POOL_MIN_SIZE", 2))
    POSTGRES_POOL_MAX_SIZE = int(os.getenv("POSTGRES_POOL_MAX_SIZE", 10))

    # Redis
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

    # MongoDB
    MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))
    MONGODB_DB = os.getenv("MONGODB_DB", "ecommerce_sessions")
    MONGODB_USER = os.getenv("MONGODB_USER", "admin")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "admin_password")

    # Application
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def postgres_url(cls):
        """Generate PostgreSQL connection URL"""
        return (
            f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@"
            f"{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
        )

    @classmethod
    def mongodb_url(cls):
        """Generate MongoDB connection URL"""
        return (
            f"mongodb://{cls.MONGODB_USER}:{cls.MONGODB_PASSWORD}@"
            f"{cls.MONGODB_HOST}:{cls.MONGODB_PORT}/{cls.MONGODB_DB}"
        )

    @classmethod
    def redis_url(cls):
        """Generate Redis connection URL"""
        if cls.REDIS_PASSWORD:
            return f"redis://:{cls.REDIS_PASSWORD}@{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"


# Singleton instance
settings = Settings()

