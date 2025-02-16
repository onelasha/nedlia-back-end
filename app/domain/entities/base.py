"""
Base entity module
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """Base entity with common fields"""

    id: Optional[str] = Field(None, description="Unique identifier")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic config"""

        arbitrary_types_allowed = True
