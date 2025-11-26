from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.db.database import get_db


# PUBLIC_INTERFACE
def get_db_session(db: Session = Depends(get_db)) -> Generator[Session, None, None]:
    """Provide a SQLAlchemy database session for request handlers via FastAPI Depends.

    Returns:
    - Generator yielding a Session which is closed automatically after the request.
    """
    yield db
