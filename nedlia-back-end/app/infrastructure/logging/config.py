"""Logging configuration for the application."""

import logging.config
import sys
from typing import Any, Dict

import structlog

from app.infrastructure.config import get_settings

def configure_logging() -> None:
    """Configure logging for the application."""
    settings = get_settings()

    # Processors for structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    if settings.logging.json_logs:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.getLevelName(settings.logging.level)
        ),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging
    logging_config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
            "console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.dev.ConsoleRenderer(),
            },
        },
        "handlers": {
            "console": {
                "level": settings.logging.level,
                "class": "logging.StreamHandler",
                "formatter": "json" if settings.logging.json_logs else "console",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": settings.logging.level,
                "propagate": True,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": settings.logging.level,
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": settings.logging.level,
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(logging_config)
