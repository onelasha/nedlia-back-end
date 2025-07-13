"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.infrastructure.persistence.database import get_session

router = APIRouter()

@router.get(
    "/health",
    summary="Health check",
    description="Check the health of the application and its dependencies"
)
async def health_check(
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Check application health."""
    # Check database connection
    try:
        await session.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "version": "0.1.0"  # This should come from settings
    }
