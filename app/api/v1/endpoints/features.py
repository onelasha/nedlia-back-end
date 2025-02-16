"""Feature flag endpoints"""

import logging

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from app.core.feature_flags import FeatureFlag

logger = logging.getLogger(__name__)

router = APIRouter()


class FeatureState(BaseModel):
    """Feature state response model"""

    name: str
    enabled: bool


def get_available_features() -> dict[str, FeatureFlag]:
    """Get available features"""
    return {
        "dark-mode": FeatureFlag("dark-mode", fallback=False),
        "beta-features": FeatureFlag("beta-features", fallback=False),
        "premium-feature": FeatureFlag("premium-feature", fallback=False),
        "error-feature": FeatureFlag("error-feature", fallback=False),
    }


@router.get("/{feature_key}", response_model=FeatureState)
def get_feature_state(feature_key: str, request: Request) -> FeatureState:
    """Get feature state"""
    features = get_available_features()
    if feature_key not in features:
        raise HTTPException(status_code=404, detail="Feature not found")

    try:
        return FeatureState(name=feature_key, enabled=features[feature_key](request))
    except HTTPException as exc:
        # Pass through HTTP exceptions from feature evaluation
        raise exc
    except (ValueError, AttributeError) as exc:
        logger.warning(
            "Error evaluating feature %s: %s",
            feature_key,
            str(exc),
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error evaluating feature {feature_key}: {str(exc)}",
        ) from exc


@router.get("/", response_model=list[FeatureState])
def get_all_features(request: Request) -> list[FeatureState]:
    """Get all feature states"""
    features = get_available_features()
    result = []

    for key, feature in features.items():
        try:
            result.append(FeatureState(name=key, enabled=feature(request)))
        except HTTPException as exc:
            # Skip features that fail to evaluate with a 500 error
            if exc.status_code == 500:
                continue
            raise exc
        except (ValueError, AttributeError) as exc:
            # Log specific errors but continue processing other features
            logger.warning(
                "Error evaluating feature %s: %s",
                key,
                str(exc),
                exc_info=True,
            )
            continue

    return result
