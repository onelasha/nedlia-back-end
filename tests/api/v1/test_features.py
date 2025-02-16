"""
Tests for feature flag endpoints
"""

from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.v1.endpoints.features import get_available_features
from app.core.feature_flags import (
    FeatureContext,
    FeatureFlag,
    feature_cache,
    get_cache_key,
)


@pytest.fixture(autouse=True)
def clear_cache():
    """Clear feature cache before each test"""
    feature_cache.clear()
    yield


@pytest.fixture
def feature_context():  # pylint: disable=redefined-outer-name
    """Feature context fixture"""
    return FeatureContext(
        user_id="test-user",
        environment="production",
        client_version="1.0.0",
    )


def test_feature_context_creation():
    """Test feature context creation"""
    context = FeatureContext(
        user_id="test-user",
        environment="production",
        client_version="1.0.0",
    )
    assert context.user_id == "test-user"
    assert context.environment == "production"
    assert context.client_version == "1.0.0"


def test_feature_flag_direct_usage(
    feature_context, mock_growthbook_instance
):  # pylint: disable=redefined-outer-name
    """Test feature flag direct usage"""
    with patch(
        "app.core.feature_flags.get_growthbook", return_value=mock_growthbook_instance
    ):
        features = get_available_features()
        feature = features["dark-mode"]
        assert feature.is_on(feature_context) is True


def test_feature_flag_caching(
    feature_context, mock_growthbook_instance
):  # pylint: disable=redefined-outer-name
    """Test feature flag caching"""
    with patch(
        "app.core.feature_flags.get_growthbook", return_value=mock_growthbook_instance
    ):
        features = get_available_features()
        feature = features["dark-mode"]
        cache_key = get_cache_key("dark-mode", feature_context)

        # First call should cache
        assert feature.is_on(feature_context) is True
        assert cache_key in feature_cache

        # Modify cache to verify it's used
        cached = feature_cache[cache_key]
        cached["value"] = False

        # Second call should use cache
        assert feature.is_on(feature_context) is False


def test_feature_flag_error_handling(
    feature_context, mock_growthbook_instance
):  # pylint: disable=redefined-outer-name
    """Test feature flag error handling"""
    with patch(
        "app.core.feature_flags.get_growthbook", return_value=mock_growthbook_instance
    ):
        features = get_available_features()
        feature = features["error-feature"]

        with pytest.raises(HTTPException) as exc_info:
            feature.is_on(feature_context)

        assert exc_info.value.status_code == 500
        assert "Error evaluating feature" in str(exc_info.value.detail)


def test_growthbook_initialization_error():
    """Test GrowthBook initialization error"""
    with patch(
        "app.core.feature_flags.GrowthBook", side_effect=ValueError("Test error")
    ):
        feature = FeatureFlag("test-feature", fallback=True)
        with pytest.raises(HTTPException) as exc_info:
            feature.is_on(FeatureContext())

        assert exc_info.value.status_code == 500
        assert "Failed to initialize feature flag service" in str(exc_info.value.detail)


def test_get_feature_state(
    client: TestClient, test_settings
):  # pylint: disable=redefined-outer-name
    """Test getting a specific feature flag state"""
    # Test always-on feature
    response = client.get(
        f"{test_settings.API_V1_STR}/features/dark-mode",
        headers={"X-User-Id": "test-user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "dark-mode"
    assert isinstance(data["enabled"], bool)

    # Test environment-based feature in production
    response = client.get(
        f"{test_settings.API_V1_STR}/features/beta-features",
        headers={"X-User-Id": "test-user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "beta-features"
    assert isinstance(data["enabled"], bool)

    # Test user-dependent feature
    response = client.get(
        f"{test_settings.API_V1_STR}/features/premium-feature",
        headers={"X-User-Id": "test-user"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "premium-feature"
    assert isinstance(data["enabled"], bool)

    # Test same feature without user
    response = client.get(f"{test_settings.API_V1_STR}/features/premium-feature")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "premium-feature"
    assert isinstance(data["enabled"], bool)

    # Test non-existent feature
    response = client.get(f"{test_settings.API_V1_STR}/features/non-existent")
    assert response.status_code == 404


def test_get_all_features(
    client: TestClient, test_settings
):  # pylint: disable=redefined-outer-name
    """Test getting all feature flag states"""
    # Test as anonymous user
    response = client.get(f"{test_settings.API_V1_STR}/features/")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(f["enabled"], bool) for f in data)

    # Test as logged-in user
    response = client.get(
        f"{test_settings.API_V1_STR}/features/",
        headers={"X-User-Id": "test-user"},
    )
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert all(isinstance(f["enabled"], bool) for f in data)


def test_feature_flag_headers(
    client: TestClient, test_settings
):  # pylint: disable=redefined-outer-name
    """Test feature flag behavior with different headers"""
    # Test with client version
    response = client.get(
        f"{test_settings.API_V1_STR}/features/dark-mode",
        headers={"X-User-Id": "test-user", "X-Client-Version": "2.0.0"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "dark-mode"
    assert isinstance(data["enabled"], bool)

    # Test with development environment override
    response = client.get(
        f"{test_settings.API_V1_STR}/features/beta-features",
        headers={"X-Environment": "development"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "beta-features"
    assert isinstance(data["enabled"], bool)
