"""User DTOs for application layer."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class UserCreateDTO(BaseModel):
    """DTO for creating a new user."""
    
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None

class UserUpdateDTO(BaseModel):
    """DTO for updating a user."""
    
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

class UserResponseDTO(BaseModel):
    """DTO for user response."""
    
    id: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""
        
        from_attributes = True
