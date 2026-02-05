"""Base model definition for SQLAlchemy models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    SQLAlchemy 2.0 style Declarative Base.
    This class will be inherited by all models.
    """

    pass
