import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio
from main import app

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
async def async_client():
    async with AsyncClient(base_url="http://testserver") as client:
        yield client
