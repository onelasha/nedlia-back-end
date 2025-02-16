"""Test configuration and fixtures"""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.v1.endpoints.features import get_available_features
from app.core.config import Settings, get_settings
from app.core.feature_flags import get_growthbook
from app.main import app


def get_test_settings() -> Settings:
    """Get test settings"""
    return Settings(
        ENV="test",
        DEBUG=True,
        GROWTHBOOK_API_HOST="https://cdn.growthbook.io",
        GROWTHBOOK_CLIENT_KEY="test-key",
        GROWTHBOOK_CACHE_TTL=60,
    )


@pytest.fixture(name="test_settings")
def fixture_test_settings() -> Settings:
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

    def load_features(self) -> None:
        """Mock load_features method"""
        # Intentionally empty - mock doesn't need to load features


@pytest.fixture(name="mock_growthbook_instance")
def fixture_mock_growthbook() -> MockGrowthBook:
    """Create a mock GrowthBook instance"""
    return MockGrowthBook()


@pytest.fixture(name="mock_features")
def fixture_mock_features():
    """Create mock feature flags"""
    return get_available_features


@pytest.fixture(name="client")
def fixture_client(
    test_settings: Settings,
    mock_growthbook_instance: MockGrowthBook,
    mock_features,
) -> TestClient:
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
