"""
API router module
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, root

api_router = APIRouter()

api_router.include_router(root.router, tags=["root"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
