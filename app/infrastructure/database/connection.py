"""
Database connection module
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

# from ...core.config import settings


class DatabaseClient:
    """Database client singleton"""

    client: AsyncIOMotorClient = None
    db: Database = None

    @classmethod
    async def connect_db(cls):
        """Connect to database"""
        # Replace with your actual MongoDB connection string
        cls.client = AsyncIOMotorClient("mongodb://localhost:27017")
        cls.db = cls.client.nedlia_db

    @classmethod
    async def close_db(cls):
        """Close database connection"""
        if cls.client is not None:
            cls.client.close()

    @classmethod
    async def get_db(cls) -> Database:
        """Get database instance"""
        return cls.db
