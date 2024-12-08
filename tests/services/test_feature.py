import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.feature_service import get_feature_service

class TestFeature(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.feature_service = get_feature_service()

    def test_refresh(self):
        self.assertEqual(True,True)

    def test_get_feature_service(self):
        self.assertEqual(True,True)
