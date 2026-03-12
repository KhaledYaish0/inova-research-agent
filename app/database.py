import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


class DatabaseConfigurationError(RuntimeError):
    """Raised when the database configuration is missing or invalid."""


@lru_cache(maxsize=1)
def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    postgres_db = os.getenv("POSTGRES_DB")
    postgres_user = os.getenv("POSTGRES_USER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    postgres_host = os.getenv("POSTGRES_HOST", "db")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")

    if postgres_db and postgres_user and postgres_password:
        return (
            f"postgresql://{postgres_user}:{postgres_password}"
            f"@{postgres_host}:{postgres_port}/{postgres_db}"
        )

    raise DatabaseConfigurationError(
        "Database configuration is missing. Set DATABASE_URL directly or define "
        "POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD in your environment/.env file."
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
Base = declarative_base()