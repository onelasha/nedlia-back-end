"""User repository interface."""

from abc import abstractmethod
from typing import Optional

from app.domain.entities.user import User
from app.domain.repositories.base import BaseRepository
from app.domain.value_objects.common import Email

class UserRepository(BaseRepository[User]):
    """Interface for user repository."""

    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email."""
        pass

    @abstractmethod
    async def email_exists(self, email: Email) -> bool:
        """Check if email exists."""
        pass
