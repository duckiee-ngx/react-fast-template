from redis.asyncio import Redis

from app.core.config import app_settings

redis_client: Redis | None = None


async def init_redis() -> Redis:
    global redis_client
    redis_client = Redis.from_url(
        app_settings.REDIS_URL(0),
        encoding="utf-8",
        decode_responses=True,
    )
    await redis_client.ping()
    return redis_client


async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None


def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis is not initialized")
    return redis_client


class RedisKeys:
    def refresh_token(self, refresh_token: str) -> str:
        return f"refresh:{refresh_token}"

    def blacklist_jti(self, jti: str) -> str:
        return f"blacklist:jti:{jti}"


redis_keys = RedisKeys()
