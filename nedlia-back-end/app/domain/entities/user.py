"""User entity implementation."""

from datetime import datetime
from typing import Any, Dict, Optional

from app.domain.entities.base import BaseEntity
from app.domain.exceptions.base import BusinessRuleViolation
from app.domain.value_objects.common import Email, Password, PhoneNumber

class User(BaseEntity):
    """User domain entity."""

    def __init__(
        self,
        email: Email,
        password: Password,
        phone: Optional[PhoneNumber] = None,
        is_active: bool = True,
        is_verified: bool = False,
        entity_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        super().__init__(entity_id, created_at, updated_at)
        self._email = email
        self._password = password
        self._phone = phone
        self._is_active = is_active
        self._is_verified = is_verified

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
