"""
Tests for feature flag endpoints
"""

from collections.abc import Generator

import pytest

from app.core.feature_flags import FeatureContext, FeatureFlag, feature_cache


@pytest.fixture(autouse=True)
def clear_cache() -> Generator[None, None, None]:
    """Clear feature cache before each test"""
    feature_cache.clear()
    yield
    feature_cache.clear()


def test_feature_flag_init() -> None:
    """Test FeatureFlag initialization"""
    feature = FeatureFlag("test_feature", fallback=False)
    assert feature.feature_key == "test_feature"
    assert feature.fallback is False


def test_feature_context_init() -> None:
    """Test FeatureContext initialization"""
    context = FeatureContext(
        user_id="test_user",
        environment="test",
        client_version="1.0.0",
    )
    assert context.user_id == "test_user"
    assert context.environment == "test"
    assert context.client_version == "1.0.0"


@pytest.mark.asyncio
async def test_feature_evaluation(  # pylint: disable=redefined-outer-name
    mock_context: FeatureContext,
) -> None:
    """Test feature flag evaluation"""
    feature = FeatureFlag("test_feature", fallback=False)
    result = feature.is_on(mock_context)
    assert isinstance(result, bool)


def test_feature_evaluation_with_context(  # pylint: disable=redefined-outer-name
    mock_context: FeatureContext,
) -> None:
    """Test feature flag evaluation with context"""
    feature = FeatureFlag("test_feature", fallback=False)
    result = feature.is_on(mock_context)
    assert isinstance(result, bool)


def test_feature_evaluation_with_invalid_key(  # pylint: disable=redefined-outer-name
    mock_context: FeatureContext,
) -> None:
    """Test feature flag evaluation with invalid key"""
    feature = FeatureFlag("invalid_feature", fallback=False)
    result = feature.is_on(mock_context)
    assert isinstance(result, bool)
    assert result is False


@pytest.mark.asyncio
async def test_feature_evaluation_async(  # pylint: disable=redefined-outer-name
    mock_context: FeatureContext,
) -> None:
    """Test async feature flag evaluation"""
    feature = FeatureFlag("test_feature", fallback=False)
    result = feature.is_on(mock_context)
    assert isinstance(result, bool)


def test_feature_evaluation_with_fallback(  # pylint: disable=redefined-outer-name
    mock_context: FeatureContext,
) -> None:
    """Test feature flag evaluation with fallback"""
    feature = FeatureFlag("test_feature", fallback=True)
    result = feature.is_on(mock_context)
    assert isinstance(result, bool)


def test_feature_evaluation_with_empty_context() -> None:
    """Test feature flag evaluation with empty context"""
    feature = FeatureFlag("test_feature", fallback=False)
    context = FeatureContext()
    result = feature.is_on(context)
    assert isinstance(result, bool)


@pytest.mark.asyncio
async def test_feature_evaluation_with_custom_attributes() -> None:
    """Test feature flag evaluation with custom attributes"""
    feature = FeatureFlag("test_feature", fallback=False)
    context = FeatureContext(
        user_id="custom_user",
        environment="custom_env",
        client_version="2.0.0",
    )
    result = feature.is_on(context)
    assert isinstance(result, bool)


def test_feature_evaluation_with_mock_features(  # pylint: disable=redefined-outer-name
    mock_context: FeatureContext,
) -> None:
    """Test feature flag evaluation with mock features"""
    feature = FeatureFlag("test_feature", fallback=False)
    result = feature.is_on(mock_context)
    assert isinstance(result, bool)
