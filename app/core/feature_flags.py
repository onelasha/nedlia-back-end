"""
Feature flag implementation using GrowthBook
"""

import logging
import time

from cachetools import TTLCache
from fastapi import HTTPException, Request
from growthbook import GrowthBook
from pydantic import BaseModel

from app.core.config import get_settings

# Initialize cache with TTL of 60 seconds
feature_cache: TTLCache = TTLCache(maxsize=100, ttl=60)

# Get logger
logger = logging.getLogger(__name__)


class FeatureContext(BaseModel):
    """Feature context for evaluation"""

    user_id: str | None = None
    environment: str = "production"
    client_version: str | None = None


def get_growthbook() -> GrowthBook:
    """
    Get GrowthBook instance

    Returns:
        GrowthBook: Initialized GrowthBook instance

    Raises:
        HTTPException: If GrowthBook initialization fails
    """
    settings = get_settings()

    try:
        return GrowthBook(
            api_host=settings.GROWTHBOOK_API_HOST,
            client_key=settings.GROWTHBOOK_CLIENT_KEY,
        )
    except Exception as e:
        logger.error("Failed to initialize GrowthBook: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to initialize feature flag service",
        ) from e


def get_cache_key(feature_key: str, context: FeatureContext) -> str:
    """
    Generate cache key for feature evaluation

    Args:
        feature_key: Feature key
        context: Feature context

    Returns:
        str: Cache key
    """
    return f"{feature_key}:{context.model_dump_json()}"


class FeatureFlag:
    """Feature flag implementation"""

    def __init__(self, feature_key: str, fallback: bool = False):
        """
        Initialize feature flag

        Args:
            feature_key: Feature key in GrowthBook
            fallback: Fallback value if evaluation fails
        """
        self.feature_key = feature_key
        self.fallback = fallback

    def is_on(self, context: FeatureContext) -> bool:
        """
        Check if feature is enabled

        Args:
            context: Feature context containing user and environment info

        Returns:
            bool: True if feature is enabled, False otherwise

        Raises:
            HTTPException: If GrowthBook initialization fails
        """
        cache_key = get_cache_key(self.feature_key, context)

        # Check cache first
        cached = feature_cache.get(cache_key)
        if cached and time.time() - cached["timestamp"] < 60:
            return cached["value"]

        try:
            # Get GrowthBook instance
            gb = get_growthbook()

            # Set context attributes
            gb.setAttributes(
                {
                    "id": context.user_id,
                    "environment": context.environment,
                    "clientVersion": context.client_version,
                }
            )
            gb.load_features()
            # Evaluate feature
            result = gb.isOn(self.feature_key)

            # Cache the result
            feature_cache[cache_key] = {
                "value": result,
                "timestamp": int(time.time()),
            }

            return result
        except (ValueError, AttributeError) as e:
            # Log the error and re-raise with more context
            logger.error(
                "Error evaluating feature flag %s: %s",
                self.feature_key,
                str(e),
                exc_info=True,
            )
            raise HTTPException(
                status_code=500,
                detail=f"Error evaluating feature {self.feature_key}: {str(e)}",
            ) from e
        except Exception as e:
            # Handle GrowthBook initialization errors
            logger.error("Failed to initialize GrowthBook: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=500,
                detail="Failed to initialize feature flag service",
            ) from e

    def __call__(self, request: Request) -> bool:
        """Make the feature flag callable as a dependency"""
        context = FeatureContext(
            user_id=request.headers.get("X-User-Id"),
            environment=request.headers.get("X-Environment", "production"),
            client_version=request.headers.get("X-Client-Version"),
        )
        return self.is_on(context)
