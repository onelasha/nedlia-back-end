"""
Feature flag service using GrowthBook.
"""
from functools import lru_cache
from growthbook import GrowthBook
from app.core.config import get_settings

class FeatureService:
    """Feature flag service singleton."""
    def __init__(self):
        self._settings = get_settings()
        self._client = GrowthBook(
            api_host=self._settings.GROWTHBOOK_API_HOST,
            client_key=self._settings.GROWTHBOOK_CLIENT_KEY,
            cache_ttl=self._settings.GROWTHBOOK_CACHE_TTL
        )
    
    def initialize(self):
        """Initialize the feature service."""
        self._client.load_features()
    
    def refresh(self):
        """Refresh feature flags."""
        self._client.load_features()
    
    def is_enabled(self, feature_key: str) -> bool:
        """Check if a feature is enabled."""
        return self._client.is_on(feature_key)
    
    def get_feature_value(self, feature_key: str, default=None):
        """Get a feature's value."""
        return self._client.get_feature_value(feature_key, default)

@lru_cache()
def get_feature_service() -> FeatureService:
    """Get the feature service singleton."""
    return FeatureService()
