"""
Tests for root endpoints
"""

from fastapi.testclient import TestClient

from app.core.config import settings


def test_root_endpoint(client: TestClient, api_v1_prefix: str):
    """Test the root endpoint returns the correct welcome message"""
    response = client.get(f"{api_v1_prefix}/")
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs_url": f"{api_v1_prefix}/docs",
    }
