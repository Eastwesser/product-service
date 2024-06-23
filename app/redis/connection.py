import os

import aioredis

REDIS_URL = os.getenv("REDIS_URL")


async def get_redis_pool():
    return await aioredis.from_url(REDIS_URL)
