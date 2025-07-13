"""User database model."""

from datetime import datetime
from typing import Optional
from pydantic import EmailStr, Field

from app.infrastructure.persistence.models.base import BaseDocument

class UserModel(BaseDocument):
    """User database model."""
    
    email: EmailStr = Field(..., unique=True, index=True)
    hashed_password: str
    phone: Optional[str] = None
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "phone"
        ]
