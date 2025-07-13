"""API route registration."""

from fastapi import APIRouter

from app.presentation.api.v1.routes.health import router as health_router
from app.presentation.api.v1.routes.users import router as users_router

# Create main router
router = APIRouter()

# Include all route modules
router.include_router(health_router, tags=["Health"])
router.include_router(users_router, prefix="/users", tags=["Users"])
