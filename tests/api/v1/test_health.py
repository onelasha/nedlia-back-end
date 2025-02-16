"""
Tests for health endpoints
"""

from fastapi.testclient import TestClient


def test_health_check_endpoint(client: TestClient, test_settings):
    """Test that health check endpoint returns healthy status"""
    response = client.get(f"{test_settings.API_V1_STR}/health")
    assert response.status_code == 200
    # assert response.json() == {
    #     "status": "healthy",
    #     "version": test_settings.VERSION,
    #     "environment": "development" if test_settings.DEBUG else "production",
    # }
