"""
Feature flag endpoints.
"""

from fastapi import APIRouter, HTTPException
from app.services.feature_service import get_feature_service

router = APIRouter()


@router.post("/refresh")
async def refresh_features():
    """Refresh feature flags from GrowthBook."""
    try:
        get_feature_service().refresh()
        return {"status": "success", "message": "Features refreshed successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to refresh features: {str(e)}"
        )


@router.get("/status/{feature_key}")
async def get_feature_status(feature_key: str):
    """Get status of a specific feature flag."""
    service = get_feature_service()
    return {
        "feature": feature_key,
        "enabled": service.is_enabled(feature_key),
        "value": service.get_feature_value(feature_key),
    }
