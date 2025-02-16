"""
Test configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Create a test client for the FastAPI application.
    """
    return TestClient(app)


@pytest.fixture
def api_v1_prefix() -> str:
    """
    Return the API v1 prefix for endpoints.
    """
    return "/api/v1"
