from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.core.config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy Declarative Base for models."""
    pass


def _build_engine_url(raw_url: str) -> str:
    """
    Normalize SQLite URLs to include proper driver arguments and file path handling.
    For SQLite, ensure check_same_thread is disabled for FastAPI threaded workers.
    """
    if raw_url.startswith("sqlite:///") or raw_url.startswith("sqlite://"):
        return raw_url
    return raw_url


# Create the SQLAlchemy engine and session factory
settings = get_settings()
DATABASE_URL = _build_engine_url(settings.DATABASE_URL)

# For SQLite we need to pass connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, future=True, connect_args=connect_args)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)


# PUBLIC_INTERFACE
def get_db() -> Generator:
    """Yield a SQLAlchemy session and ensure it is closed after request lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db(drop_all: bool = False) -> None:
    """
    Initialize the database by creating all tables.

    Parameters:
    - drop_all: If True, drops all existing tables before creating them (use with caution).
    """
    # Import models so that metadata is populated
    from src.db import models  # noqa: F401

    if drop_all:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
