"""Test cases for the feature service and related endpoints."""

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.feature_service import get_feature_service


class TestFeature(unittest.TestCase):
    """Test cases for feature-related endpoints and services."""

    def setUp(self):
        """Initialize test client and feature service."""
        self.client = TestClient(app)
        self.feature_service = get_feature_service()

    def test_get_feature_service(self):
        """Test the feature refresh endpoint."""
        response = self.client.post("/v1/features/refresh")
        self.assertEqual(response.status_code, 200)

    def test_get_feature_status(self):
        """Test the feature status endpoint."""
        response = self.client.get("/v1/features/status/test-feature")
        self.assertEqual(response.status_code, 200)
