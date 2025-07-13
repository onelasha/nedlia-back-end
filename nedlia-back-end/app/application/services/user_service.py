"""User service implementation."""

from typing import List, Optional

from app.application.dtos.user import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.domain.entities.user import User
from app.domain.exceptions.base import ConflictError, EntityNotFound
from app.domain.repositories.user import UserRepository
from app.domain.value_objects.common import Email, Password, PhoneNumber

class UserService:
    """User service for handling user-related operations."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._repository = user_repository

    async def create_user(self, user_data: UserCreateDTO) -> UserResponseDTO:
        """Create a new user."""
        # Check if email exists
        email = Email(user_data.email)
        if await self._repository.email_exists(email):
            raise ConflictError(f"Email {email.value} already exists")

        # Create user entity
        user = User(
            email=email,
            password=Password(user_data.password),
            phone=PhoneNumber(user_data.phone) if user_data.phone else None
        )

        # Save user
        created_user = await self._repository.add(user)
        return UserResponseDTO.from_orm(created_user)

    async def get_user(self, user_id: str) -> UserResponseDTO:
        """Get user by ID."""
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise EntityNotFound(f"User {user_id} not found")
        return UserResponseDTO.from_orm(user)

    async def get_user_by_email(self, email: str) -> Optional[UserResponseDTO]:
        """Get user by email."""
        user = await self._repository.get_by_email(Email(email))
        return UserResponseDTO.from_orm(user) if user else None

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[UserResponseDTO]:
        """List users with pagination."""
        users = await self._repository.list(skip=skip, limit=limit)
        return [UserResponseDTO.from_orm(user) for user in users]

    async def update_user(self, user_id: str, user_data: UserUpdateDTO) -> UserResponseDTO:
        """Update user."""
        # Get existing user
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise EntityNotFound(f"User {user_id} not found")

        # Update fields
        if user_data.email:
            new_email = Email(user_data.email)
            if await self._repository.email_exists(new_email):
                raise ConflictError(f"Email {new_email.value} already exists")
            user.update_email(new_email)

        if user_data.phone:
            user.update_phone(PhoneNumber(user_data.phone))

        if user_data.password:
            user.update_password(Password(user_data.password))

        # Save changes
        updated_user = await self._repository.update(user)
        return UserResponseDTO.from_orm(updated_user)

    async def delete_user(self, user_id: str) -> bool:
        """Delete user."""
        if not await self._repository.exists(user_id):
            raise EntityNotFound(f"User {user_id} not found")
        return await self._repository.delete(user_id)

    async def activate_user(self, user_id: str) -> UserResponseDTO:
        """Activate user."""
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise EntityNotFound(f"User {user_id} not found")
        
        user.activate()
        updated_user = await self._repository.update(user)
        return UserResponseDTO.from_orm(updated_user)

    async def deactivate_user(self, user_id: str) -> UserResponseDTO:
        """Deactivate user."""
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise EntityNotFound(f"User {user_id} not found")
        
        user.deactivate()
        updated_user = await self._repository.update(user)
        return UserResponseDTO.from_orm(updated_user)

    async def verify_user(self, user_id: str) -> UserResponseDTO:
        """Verify user."""
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise EntityNotFound(f"User {user_id} not found")
        
        user.verify()
        updated_user = await self._repository.update(user)
        return UserResponseDTO.from_orm(updated_user)
