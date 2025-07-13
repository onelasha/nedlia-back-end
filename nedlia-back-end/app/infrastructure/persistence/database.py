"""MongoDB database configuration and initialization."""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.application.services.user_service import UserService
from app.infrastructure.config import get_settings
from app.infrastructure.persistence.models.user import UserModel
from app.infrastructure.persistence.repositories.user import MongoUserRepository

settings = get_settings()

async def init_mongodb():
    """Initialize MongoDB connection and Beanie ODM."""
    # Create motor client
    client = AsyncIOMotorClient(
        settings.database.url,
        minPoolSize=settings.database.min_pool_size,
        maxPoolSize=settings.database.max_pool_size,
        maxIdleTimeMS=settings.database.max_idle_time_ms,
        connectTimeoutMS=settings.database.connect_timeout_ms,
        serverSelectionTimeoutMS=settings.database.server_selection_timeout_ms
    )
    
    # Initialize Beanie with the document models
    await init_beanie(
        database=client[settings.database.db_name],
        document_models=[
            UserModel
        ]
    )

async def get_user_repository() -> MongoUserRepository:
    """Get user repository instance."""
    return MongoUserRepository()

async def get_user_service(
    repository: MongoUserRepository = None
) -> UserService:
    """Get user service instance."""
    if repository is None:
        repository = await get_user_repository()
    return UserService(repository)
