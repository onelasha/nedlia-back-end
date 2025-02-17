"""
Database connection module
"""

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings


class DatabaseClient:
    """Database client singleton"""

    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect_db(cls) -> None:
        """Connect to database"""
        settings = get_settings()
        cls.client = AsyncIOMotorClient(settings.MONGODB_URI)
        cls.db = cls.client.get_database("nedlia_db")

    @classmethod
    async def close_db(cls) -> None:
        """Close database connection"""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None

    @classmethod
    def get_db(cls) -> Optional[AsyncIOMotorDatabase]:
        """Get database instance"""
        return cls.db
