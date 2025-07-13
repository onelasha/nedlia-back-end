"""Database configuration and session management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from app.application.services.user_service import UserService
from app.infrastructure.config import get_settings
from app.infrastructure.persistence.repositories.user import SQLAlchemyUserRepository

# Create async engine
settings = get_settings()
engine = create_async_engine(
    str(settings.database.url),
    **settings.get_database_settings()
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()

@asynccontextmanager
async def get_transaction() -> AsyncGenerator[AsyncSession, None]:
    """Get database transaction."""
    async with async_session_factory() as session:
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

async def get_user_repository(
    session: AsyncSession = next(get_session())
) -> SQLAlchemyUserRepository:
    """Get user repository instance."""
    return SQLAlchemyUserRepository(session)

async def get_user_service(
    repository: SQLAlchemyUserRepository = next(get_user_repository())
) -> UserService:
    """Get user service instance."""
    return UserService(repository)
