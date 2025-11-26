import os
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Default to a local SQLite database file within the container workspace
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./notes.db")


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance to avoid re-parsing environment variables."""
    return Settings()
