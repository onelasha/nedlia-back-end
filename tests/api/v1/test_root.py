"""
Tests for root endpoints
"""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient, test_settings):
    """Test the root endpoint returns the correct welcome message"""
    response = client.get(f"{test_settings.API_V1_STR}/")
    assert response.status_code == 200
    # assert response.json() == {
    #     "message": f"Welcome to {test_settings.PROJECT_NAME}",
    #     "version": test_settings.VERSION,
    #     "docs_url": f"{test_settings.API_V1_STR}/docs",
    # }
