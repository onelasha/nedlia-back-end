"""Base SQLAlchemy model."""

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass
