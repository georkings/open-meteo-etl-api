"""Database session management."""

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # REQUIRED for SQLite
)

SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Yield a database session and ensure it's closed after use."""
    db = SessionLocal()
    logger.debug("Database session created.")
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session encountered an error: {e}")
        raise
    finally:
        db.close()
        logger.debug("Database session closed.")
