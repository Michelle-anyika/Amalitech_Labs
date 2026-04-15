import os
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL settings
POSTGRES_DB = os.getenv("POSTGRES_DB", "social_media_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "social_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "social_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6380))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# MongoDB settings
MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "admin")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin_password")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27018")
MONGO_DB = os.getenv("MONGO_INITDB_DATABASE", "social_activity")
MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
