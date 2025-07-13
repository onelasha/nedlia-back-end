"""Base repository interface."""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from app.domain.entities.base import BaseEntity

T = TypeVar('T', bound=BaseEntity)

class BaseRepository(ABC, Generic[T]):
    """Abstract base class for all repositories."""

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Retrieve an entity by its ID."""
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> List[T]:
        """List entities with pagination."""
        pass

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add a new entity."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete an entity by its ID."""
        pass

    @abstractmethod
    async def exists(self, entity_id: str) -> bool:
        """Check if an entity exists."""
        pass
