"""
API router configuration
"""

from fastapi import APIRouter

from app.api.v1.endpoints import features, health, root

# Create API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(root.router, tags=["root"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(features.router, prefix="/features", tags=["features"])
