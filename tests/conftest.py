"""Test configuration and fixtures"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.v1.endpoints.features import get_available_features
from app.core.config import Settings, get_settings
from app.core.feature_flags import get_growthbook
from app.main import app


def get_test_settings():
    """Get test settings"""
    return Settings(
        DEBUG=True,
        GROWTHBOOK_API_HOST="https://cdn.growthbook.io",
        GROWTHBOOK_CLIENT_KEY="test-key",
        GROWTHBOOK_CACHE_TTL=1,
    )


@pytest.fixture
def test_settings():
    """Test settings fixture"""
    return get_test_settings()


class MockGrowthBook:
    """Mock GrowthBook implementation for testing"""

    def __init__(self):
        """Initialize mock GrowthBook"""
        self.attributes = {}

    def set_attributes(self, attributes: dict) -> None:
        """Set context attributes"""
        self.attributes = attributes

    def is_on(self, key: str) -> bool:
        """Check if feature is enabled"""
        if key == "dark-mode":
            return True
        if key == "beta-features":
            return self.attributes.get("environment") == "development"
        if key == "premium-feature":
            return self.attributes.get("id") is not None
        if key == "error-feature":
            raise ValueError("Test error")
        return False

    # GrowthBook API compatibility methods
    def setAttributes(self, attributes: dict) -> None:  # pylint: disable=C0103
        """GrowthBook API compatibility method"""
        return self.set_attributes(attributes)

    def isOn(self, key: str) -> bool:  # pylint: disable=C0103
        """GrowthBook API compatibility method"""
        return self.is_on(key)


@pytest.fixture
def mock_growthbook_instance():
    """Create a mock GrowthBook instance"""
    return MockGrowthBook()


@pytest.fixture
def mock_features():
    """Create mock feature flags"""
    return get_available_features


@pytest.fixture
def client(
    test_settings, mock_growthbook_instance, mock_features
):  # pylint: disable=redefined-outer-name
    """Test client fixture"""
    app.dependency_overrides[get_settings] = lambda: test_settings
    app.dependency_overrides[get_growthbook] = lambda: mock_growthbook_instance
    app.dependency_overrides[get_available_features] = mock_features
    with TestClient(app) as test_client:
        with patch(
            "app.core.feature_flags.get_growthbook",
            return_value=mock_growthbook_instance,
        ):
            yield test_client
    app.dependency_overrides.clear()
