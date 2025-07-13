"""User profile entity."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import EmailStr, Field

from app.domain.entities.base import BaseEntity

class User(BaseEntity):
    """User profile entity synchronized with Okta."""
    
    # Core fields
    email: EmailStr
    first_name: str
    last_name: str
    
    # Okta integration
    okta_id: str
    is_active: bool = True
    last_sync: datetime = Field(default_factory=datetime.utcnow)
    
    # Extended profile
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    locale: str = "en-US"
    timezone: str = "UTC"
    
    # Custom attributes
    preferences: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def update_from_okta(self, okta_profile: dict) -> None:
        """Update user profile from Okta data."""
        self.email = okta_profile.get("email", self.email)
        self.first_name = okta_profile.get("firstName", self.first_name)
        self.last_name = okta_profile.get("lastName", self.last_name)
        self.phone = okta_profile.get("mobilePhone", self.phone)
        self.locale = okta_profile.get("locale", self.locale)
        self.timezone = okta_profile.get("timezone", self.timezone)
        self.last_sync = datetime.utcnow()
        
        # Update custom attributes if present
        custom_attrs = okta_profile.get("customAttributes", {})
        if custom_attrs:
            self.metadata.update(custom_attrs)
    
    def to_okta_profile(self) -> dict:
        """Convert to Okta profile format."""
        return {
            "email": self.email,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "mobilePhone": self.phone,
            "locale": self.locale,
            "timezone": self.timezone,
            "customAttributes": self.metadata
        }

    @property
    def email(self) -> Email:
        """Get user email."""
        return self._email

    @property
    def phone(self) -> Optional[PhoneNumber]:
        """Get user phone number."""
        return self._phone

    @property
    def is_active(self) -> bool:
        """Get user active status."""
        return self._is_active

    @property
    def is_verified(self) -> bool:
        """Get user verification status."""
        return self._is_verified

    def activate(self) -> None:
        """Activate the user."""
        if self._is_active:
            raise BusinessRuleViolation("User is already active")
        self._is_active = True
        self._update_timestamp()

    def deactivate(self) -> None:
        """Deactivate the user."""
        if not self._is_active:
            raise BusinessRuleViolation("User is already inactive")
        self._is_active = False
        self._update_timestamp()

    def verify(self) -> None:
        """Mark user as verified."""
        if self._is_verified:
            raise BusinessRuleViolation("User is already verified")
        self._is_verified = True
        self._update_timestamp()

    def update_email(self, new_email: Email) -> None:
        """Update user email."""
        if self._email == new_email:
            raise BusinessRuleViolation("New email is same as current")
        self._email = new_email
        self._is_verified = False  # Require re-verification
        self._update_timestamp()

    def update_phone(self, new_phone: Optional[PhoneNumber]) -> None:
        """Update user phone number."""
        if self._phone == new_phone:
            raise BusinessRuleViolation("New phone is same as current")
        self._phone = new_phone
        self._update_timestamp()

    def update_password(self, new_password: Password) -> None:
        """Update user password."""
        if self._password.value == new_password.value:
            raise BusinessRuleViolation("New password is same as current")
        self._password = new_password
        self._update_timestamp()

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        data = super().to_dict()
        data.update({
            "email": self._email.value,
            "phone": str(self._phone) if self._phone else None,
            "is_active": self._is_active,
            "is_verified": self._is_verified
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        """Create user from dictionary."""
        return cls(
            email=Email(data["email"]),
            password=Password(data.get("password", ""), data.get("hashed_password")),
            phone=PhoneNumber(data["phone"]) if data.get("phone") else None,
            is_active=data.get("is_active", True),
            is_verified=data.get("is_verified", False),
            entity_id=data.get("id"),
            created_at=datetime.fromisoformat(data["created_at"]) if "created_at" in data else None,
            updated_at=datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else None
        )
