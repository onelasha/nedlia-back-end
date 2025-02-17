"""
Main application module
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """
    Handle startup and shutdown events
    """
    yield


def create_application() -> FastAPI:
    """Create FastAPI application"""
    settings = get_settings()

    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    # Set CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = create_application()

if __name__ == "__main__":
    import uvicorn

    # Use localhost by default for security
    HOST = "127.0.0.1"  # More secure default
    PORT = 8000

    # Only bind to all interfaces if explicitly set in production
    _local_settings = get_settings()
    if not _local_settings.DEBUG and _local_settings.ENV == "production":
        HOST = "0.0.0.0"  # nosec B104 # Intentional for production deployment

    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=_local_settings.DEBUG)
