"""
Tests for health endpoints
"""

from fastapi.testclient import TestClient

from app.core.config import settings


def test_health_check_endpoint(client: TestClient, api_v1_prefix: str):
    """Test that health check endpoint returns healthy status"""
    response = client.get(f"{api_v1_prefix}/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": "development" if settings.DEBUG else "production",
    }
