"""Base value object implementation."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class ValueObject(ABC):
    """Abstract base class for value objects.
    
    Value objects are immutable and their equality is based on their attributes,
    not their identity.
    """

    def __eq__(self, other: Any) -> bool:
        """Value objects are equal if all their attributes are equal."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Hash based on the object's attributes."""
        return hash(tuple(sorted(self.__dict__.items())))

    @abstractmethod
    def validate(self) -> None:
        """Validate the value object's invariants.
        
        Raises:
            ValidationError: If validation fails.
        """
        pass
