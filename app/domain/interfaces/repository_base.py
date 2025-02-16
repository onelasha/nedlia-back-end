"""
Base repository interface
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.base import BaseEntity


class IRepository[T: BaseEntity](ABC):
    """Base repository interface"""

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> List[T]:
        """Get all entities"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an entity"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete an entity"""
        raise NotImplementedError
