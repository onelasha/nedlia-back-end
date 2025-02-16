"""
FastAPI application main module
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.infrastructure.database.connection import DatabaseClient


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Handle application startup and shutdown events.
    The FastAPI app parameter is not used but required by the framework.
    """
    # Startup
    await DatabaseClient.connect_db()
    yield
    # Shutdown
    await DatabaseClient.close_db()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Nedlia Backend API with Clean Architecture",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import asyncio

    from hypercorn.asyncio import serve
    from hypercorn.config import Config

    config = Config()
    config.bind = ["0.0.0.0:8000"]
    asyncio.run(serve(app, config))
