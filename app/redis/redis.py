import json

import aioredis

from app.models.pydantic_models import Product


async def get_redis():
    redis = await aioredis.from_url("redis://localhost")
    return redis


async def set_cache(key: str, value: Product):
    redis = await get_redis()
    await redis.set(key, json.dumps({
        "id": value.id,
        "name": value.name,
        "description": value.description,
        "price": value.price
    }))
    await redis.close()


async def get_cache(key: str) -> Product:
    redis = await get_redis()
    value = await redis.get(key)
    await redis.close()
    if value:
        data = json.loads(value)
        return Product(**data)
    return None
