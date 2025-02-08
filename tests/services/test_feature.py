import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.feature_service import get_feature_service


class TestFeature(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.feature_service = get_feature_service()

    def test_get_feature_service(self):
        response = self.client.post("/v1/features/refresh")
        self.assertEqual(response.status_code, 200)

    def test_get_feature_status(self):
        response = self.client.get("/v1/features/status/test-feature")
        self.assertEqual(response.status_code, 200)
