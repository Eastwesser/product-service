import asyncio
import os
import sys

import pytest
from httpx import AsyncClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.rabbit.rabbit import send_message
from app.redis.redis import set_cache, get_cache


@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Product Service"}


@pytest.mark.asyncio
async def test_create_product():
    product_data = {"name": "Test Product", "description": "A test product", "price": 9.99}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"


async def test_services():
    # Test sending a message
    await send_message("Test message")
    print("Message sent to RabbitMQ")

    # Test setting and getting cache
    await set_cache("test_key", "test_value")
    value = await get_cache("test_key")
    print(f"Value from Redis: {value}")  # Should print "test_value"


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(app=app, base_url="http://localhost:8002") as ac:
        response = await ac.get("/")
        assert response.status_code == 200


if __name__ == "__main__":
    asyncio.run(test_services())
