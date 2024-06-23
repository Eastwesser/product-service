import json

from app.redis.connection import get_redis_pool  # adjust import path as per your Redis setup

from app.models.models import Product  # make sure this imports the correct Product model


async def set_cache(key: str, value: Product):
    redis = await get_redis_pool()
    if isinstance(value, dict):
        value = Product(**value)
    await redis.set(key, json.dumps({
        "id": value.id,
        "name": value.name,
        "description": value.description,
        "price": value.price
    }))


async def get_cache(key: str):
    redis = await get_redis_pool()
    cached_value = await redis.get(key)
    if cached_value:
        return json.loads(cached_value)
    return None
