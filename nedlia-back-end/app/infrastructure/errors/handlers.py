"""Error handlers for the application."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.domain.exceptions.base import (
    BusinessRuleViolation,
    ConflictError,
    EntityNotFound,
    ValidationError
)

def register_error_handlers(app: FastAPI) -> None:
    """Register error handlers with the FastAPI application."""

    @app.exception_handler(ValidationError)
    async def validation_error_handler(
        request: Request,
        exc: ValidationError
    ) -> JSONResponse:
        """Handle domain validation errors."""
        return JSONResponse(
            status_code=400,
            content={
                "error": "Validation Error",
                "detail": str(exc),
                "request_id": getattr(request.state, "request_id", None)
            }
        )

    @app.exception_handler(BusinessRuleViolation)
    async def business_rule_error_handler(
        request: Request,
        exc: BusinessRuleViolation
    ) -> JSONResponse:
        """Handle business rule violations."""
        return JSONResponse(
            status_code=400,
            content={
                "error": "Business Rule Violation",
                "detail": str(exc),
                "request_id": getattr(request.state, "request_id", None)
            }
        )

    @app.exception_handler(EntityNotFound)
    async def not_found_error_handler(
        request: Request,
        exc: EntityNotFound
    ) -> JSONResponse:
        """Handle entity not found errors."""
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "detail": str(exc),
                "request_id": getattr(request.state, "request_id", None)
            }
        )

    @app.exception_handler(ConflictError)
    async def conflict_error_handler(
        request: Request,
        exc: ConflictError
    ) -> JSONResponse:
        """Handle conflict errors."""
        return JSONResponse(
            status_code=409,
            content={
                "error": "Conflict",
                "detail": str(exc),
                "request_id": getattr(request.state, "request_id", None)
            }
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request,
        exc: IntegrityError
    ) -> JSONResponse:
        """Handle database integrity errors."""
        return JSONResponse(
            status_code=409,
            content={
                "error": "Database Integrity Error",
                "detail": "A database constraint was violated.",
                "request_id": getattr(request.state, "request_id", None)
            }
        )

    @app.exception_handler(Exception)
    async def general_error_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """Handle all other exceptions."""
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": "An unexpected error occurred.",
                "request_id": getattr(request.state, "request_id", None)
            }
        )
