"""
API v1 router configuration.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import features, health

# Create v1 router
router = APIRouter(prefix="/v1")

# Add routes
router.include_router(
    health.router,
    prefix="/health",
    tags=["health"]
)

router.include_router(
    features.router,
    prefix="/features",
    tags=["features"]
)
