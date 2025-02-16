"""
Root endpoint
"""

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint"""
    settings = get_settings()
    return {"name": settings.PROJECT_NAME, "message": "Welcome to Nedlia Backend API"}
