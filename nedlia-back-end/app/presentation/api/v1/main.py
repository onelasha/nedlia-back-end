"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.infrastructure.config import get_settings
from app.infrastructure.errors.handlers import register_error_handlers
from app.infrastructure.logging.config import configure_logging
from app.infrastructure.middleware.logging import RequestLoggingMiddleware
from app.infrastructure.middleware.metrics import PrometheusMiddleware
from app.presentation.api.v1.routes import router as api_router

def create_application() -> FastAPI:
    """Create FastAPI application."""
    # Configure logging
    configure_logging()
    
    # Get settings
    settings = get_settings()
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.api.title,
        description=settings.api.description,
        version=settings.api.version,
        debug=settings.api.debug,
        docs_url=settings.api.docs_url,
        openapi_url=settings.api.openapi_url
    )

    # Register error handlers
    register_error_handlers(app)

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add logging middleware
    app.add_middleware(RequestLoggingMiddleware)

    # Add metrics middleware if enabled
    if settings.metrics_enabled:
        app.add_middleware(PrometheusMiddleware)
        metrics_app = make_asgi_app()
        app.mount("/metrics", metrics_app)

    # Add routes
    app.include_router(api_router, prefix="/api/v1")

    return app

# Create application instance
app = create_application()
