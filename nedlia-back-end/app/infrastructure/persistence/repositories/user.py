"""MongoDB implementation of user repository."""

from typing import List, Optional
from uuid import uuid4

from app.domain.entities.user import User
from app.domain.repositories.user import UserRepository
from app.domain.value_objects.common import Email, Password, PhoneNumber
from app.infrastructure.persistence.models.user import UserModel

class MongoUserRepository(UserRepository):
    """MongoDB implementation of user repository using Beanie ODM."""

    async def add(self, entity: User) -> User:
        """Add a new user."""
        model = self._to_model(entity)
        await model.save_document()
        return self._to_entity(model)

    async def get_by_id(self, entity_id: str) -> Optional[User]:
        """Get user by ID."""
        model = await UserModel.get(entity_id)
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email."""
        model = await UserModel.find_one(UserModel.email == email.value)
        return self._to_entity(model) if model else None

    async def list(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List users with pagination."""
        models = await UserModel.find_all().skip(skip).limit(limit).to_list()
        return [self._to_entity(model) for model in models]

    async def update(self, entity: User) -> User:
        """Update an existing user."""
        model = await UserModel.get(entity.id)
        if model:
            updated_model = self._to_model(entity)
            for key, value in updated_model.__dict__.items():
                if not key.startswith('_'):
                    setattr(model, key, value)
            await model.save_document()
            return self._to_entity(model)
        return entity

    async def delete(self, entity_id: str) -> bool:
        """Delete a user."""
        model = await UserModel.get(entity_id)
        if model:
            await model.delete()
            return True
        return False

    async def exists(self, entity_id: str) -> bool:
        """Check if a user exists."""
        model = await UserModel.get(entity_id)
        return model is not None

    async def email_exists(self, email: Email) -> bool:
        """Check if email exists."""
        model = await UserModel.find_one(UserModel.email == email.value)
        return model is not None

    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to database model."""
        return UserModel(
            id=entity.id,
            email=entity.email.value,
            hashed_password=entity.password.value,
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
