"""
Health check endpoints.
"""
from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter()

@router.get("")
async def health_check():
    """Basic health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION
    }
