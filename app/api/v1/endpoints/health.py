"""
Health check endpoints
"""

from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production",
    }
