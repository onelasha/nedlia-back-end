"""SQLAlchemy implementation of user repository."""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository
from app.domain.value_objects.common import Email, Password, PhoneNumber
from app.infrastructure.persistence.models.user import UserModel
from app.infrastructure.persistence.repositories.base import SQLAlchemyRepository

class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy implementation of user repository."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def get_by_id(self, entity_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self._session.get(UserModel, entity_id)
        return self._to_entity(result) if result else None

    async def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.value)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List users with pagination."""
        result = await self._session.execute(
            select(UserModel)
            .offset(skip)
            .limit(limit)
        )
        return [self._to_entity(model) for model in result.scalars().all()]

    async def add(self, entity: User) -> User:
        """Add a new user."""
        model = self._to_model(entity)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def update(self, entity: User) -> User:
        """Update an existing user."""
        model = await self._session.get(UserModel, entity.id)
        if model:
            updated_model = self._to_model(entity)
            for key, value in updated_model.__dict__.items():
                if not key.startswith('_'):
                    setattr(model, key, value)
            await self._session.flush()
            await self._session.refresh(model)
            return self._to_entity(model)
        return entity

    async def delete(self, entity_id: str) -> bool:
        """Delete a user."""
        model = await self._session.get(UserModel, entity_id)
        if model:
            await self._session.delete(model)
            await self._session.flush()
            return True
        return False

    async def exists(self, entity_id: str) -> bool:
        """Check if a user exists."""
        result = await self._session.get(UserModel, entity_id)
        return result is not None

    async def email_exists(self, email: Email) -> bool:
        """Check if email exists."""
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email.value)
        )
        return result.scalar_one_or_none() is not None

    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=entity.id,
            email=entity.email.value,
            hashed_password=entity._password.hashed or entity._password.value,  # In practice, this should be properly hashed
            phone=str(entity.phone) if entity.phone else None,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def _to_entity(self, model: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            email=Email(model.email),
            password=Password("", model.hashed_password),
            phone=PhoneNumber(model.phone) if model.phone else None,
            is_active=model.is_active,
            is_verified=model.is_verified,
            entity_id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
