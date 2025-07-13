"""Common value objects used across the domain."""

import re
from dataclasses import dataclass
from typing import Optional

from app.domain.exceptions.validation import ValidationError
from app.domain.value_objects.base import ValueObject

@dataclass(frozen=True)
class Email(ValueObject):
    """Email value object with validation."""
    
    value: str

    def validate(self) -> None:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, self.value):
            raise ValidationError(f"Invalid email format: {self.value}")

    @property
    def domain(self) -> str:
        """Get email domain."""
        return self.value.split('@')[1]

    @property
    def local_part(self) -> str:
        """Get email local part."""
        return self.value.split('@')[0]

@dataclass(frozen=True)
class Password(ValueObject):
    """Password value object with validation."""
    
    value: str
    hashed: Optional[str] = None

    def validate(self) -> None:
        """Validate password requirements."""
        if len(self.value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in self.value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in self.value):
            raise ValidationError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in self.value):
            raise ValidationError("Password must contain at least one number")

@dataclass(frozen=True)
class PhoneNumber(ValueObject):
    """Phone number value object with validation."""
    
    value: str
    country_code: str = "1"  # Default to US/Canada

    def validate(self) -> None:
        """Validate phone number format."""
        pattern = r'^\+?1?\d{9,15}$'
        if not re.match(pattern, self.value):
            raise ValidationError(f"Invalid phone number format: {self.value}")

    def __str__(self) -> str:
        """Format phone number with country code."""
        return f"+{self.country_code}{self.value.lstrip('+').lstrip('1')}"
