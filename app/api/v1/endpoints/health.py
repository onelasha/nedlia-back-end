"""
Health check endpoint
"""

from typing import Dict

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    settings = get_settings()
    return {"name": settings.PROJECT_NAME, "status": "healthy"}
