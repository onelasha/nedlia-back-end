"""
Application startup and shutdown events.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services.feature_service import get_feature_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI application"""
    # Startup
    print(f"Starting up...{app.name}")
    feature_service = get_feature_service()
    feature_service.initialize()
    yield
    # Shutdown
    print("Shutting down...")
