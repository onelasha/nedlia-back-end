"""User routes."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos.user import UserCreateDTO, UserResponseDTO, UserUpdateDTO
from app.application.services.user_service import UserService
from app.domain.exceptions.base import (
    BusinessRuleViolation,
    ConflictError,
    EntityNotFound,
    ValidationError
)
from app.infrastructure.persistence.database import get_user_service

router = APIRouter()

@router.post(
    "/users",
    response_model=UserResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information"
)
async def create_user(
    user_data: UserCreateDTO,
    user_service: UserService = Depends(get_user_service)
) -> UserResponseDTO:
    """Create a new user."""
    try:
        return await user_service.create_user(user_data)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.get(
    "/users/{user_id}",
    response_model=UserResponseDTO,
    summary="Get user by ID",
    description="Get detailed information about a specific user"
)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> UserResponseDTO:
    """Get user by ID."""
    try:
        return await user_service.get_user(user_id)
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.get(
    "/users",
    response_model=List[UserResponseDTO],
    summary="List users",
    description="Get a list of users with pagination"
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service)
) -> List[UserResponseDTO]:
    """List users with pagination."""
    return await user_service.list_users(skip=skip, limit=limit)

@router.put(
    "/users/{user_id}",
    response_model=UserResponseDTO,
    summary="Update user",
    description="Update user information"
)
async def update_user(
    user_id: str,
    user_data: UserUpdateDTO,
    user_service: UserService = Depends(get_user_service)
) -> UserResponseDTO:
    """Update user."""
    try:
        return await user_service.update_user(user_id, user_data)
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except (ValidationError, BusinessRuleViolation) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user"
)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> None:
    """Delete user."""
    try:
        await user_service.delete_user(user_id)
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.post(
    "/users/{user_id}/activate",
    response_model=UserResponseDTO,
    summary="Activate user",
    description="Activate a user account"
)
async def activate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> UserResponseDTO:
    """Activate user."""
    try:
        return await user_service.activate_user(user_id)
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post(
    "/users/{user_id}/deactivate",
    response_model=UserResponseDTO,
    summary="Deactivate user",
    description="Deactivate a user account"
)
async def deactivate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service)
) -> UserResponseDTO:
    """Deactivate user."""
    try:
        return await user_service.deactivate_user(user_id)
    except EntityNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except BusinessRuleViolation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
