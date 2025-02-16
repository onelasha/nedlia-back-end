"""
Base service module
"""

from typing import List, Optional

from app.domain.entities.base import BaseEntity
from app.domain.interfaces.repository_base import IRepository


class BaseService[T: BaseEntity]:
    """Base service with common CRUD operations"""

    def __init__(self, repository: IRepository[T]):
        self.repository = repository

    async def create(self, entity: T) -> T:
        """Create a new entity"""
        return await self.repository.create(entity)

    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by id"""
        return await self.repository.get_by_id(entity_id)

    async def get_all(self) -> List[T]:
        """Get all entities"""
        return await self.repository.get_all()

    async def update(self, entity: T) -> T:
        """Update an entity"""
        return await self.repository.update(entity)

    async def delete(self, entity_id: str) -> bool:
        """Delete an entity"""
        return await self.repository.delete(entity_id)
