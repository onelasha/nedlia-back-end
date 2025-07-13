"""User profile model for MongoDB using Beanie ODM."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import EmailStr, Field
from beanie import Document, Indexed

class UserModel(Document):
    """User profile model synchronized with Okta."""
    
    # Core fields
    email: Indexed(EmailStr, unique=True)
    first_name: str
    last_name: str
    
    # Okta integration
    okta_id: Indexed(str, unique=True)
    is_active: bool = Field(default=True)
    last_sync: datetime = Field(default_factory=datetime.utcnow)
    
    # Extended profile
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    locale: str = Field(default="en-US")
    timezone: str = Field(default="UTC")
    
    # Custom attributes
    preferences: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "user_profiles"
        indexes = [
            "email",
            "okta_id",
            "phone"
        ]
    
    def to_entity(self) -> "User":
        """Convert to domain entity."""
        from app.domain.entities.user import User
        return User(
            id=str(self.id),
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            okta_id=self.okta_id,
            is_active=self.is_active,
            phone=self.phone,
            avatar_url=self.avatar_url,
            locale=self.locale,
            timezone=self.timezone,
            preferences=self.preferences,
            metadata=self.metadata,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_entity(cls, user: "User") -> "UserModel":
        """Create from domain entity."""
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            okta_id=user.okta_id,
            is_active=user.is_active,
            phone=user.phone,
            avatar_url=user.avatar_url,
            locale=user.locale,
            timezone=user.timezone,
            preferences=user.preferences,
            metadata=user.metadata,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
