"""
FastAPI application main module
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.infrastructure.database.connection import DatabaseClient

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Nedlia Backend API with Clean Architecture",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection"""
    await DatabaseClient.connect_db()


@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection"""
    await DatabaseClient.close_db()


@app.get(f"{settings.API_V1_STR}/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
    }


@app.get(f"{settings.API_V1_STR}/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import asyncio

    import hypercorn.asyncio

    config = hypercorn.Config()
    config.bind = ["0.0.0.0:8000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
