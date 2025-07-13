"""Base MongoDB document model."""

from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field

class BaseDocument(Document):
    """Base class for all MongoDB documents."""
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    class Settings:
        use_state_management = True
        validate_on_save = True
    
    async def save_document(self) -> None:
        """Save document and update timestamps."""
        self.updated_at = datetime.utcnow()
        await self.save()
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
