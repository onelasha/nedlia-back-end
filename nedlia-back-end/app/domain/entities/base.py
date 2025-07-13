"""Base entity class for domain models."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional
import uuid

class BaseEntity(ABC):
    """Abstract base class for all domain entities."""
    
    def __init__(
        self,
        entity_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> None:
        self._id = entity_id or str(uuid.uuid4())
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or self._created_at

    @property
    def id(self) -> str:
        """Get entity ID."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get last update timestamp."""
        return self._updated_at

    def _update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        self._updated_at = datetime.utcnow()

    def __eq__(self, other: Any) -> bool:
        """Entities are equal if their IDs are equal."""
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on entity ID."""
        return hash(self.id)

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseEntity":
        """Create entity from dictionary."""
        pass
