"""Redis — только подключение и пинг (M1.9). Кеш-логики нет (она в M8).

Клиент — единый пул, не пересоздаётся на запрос. Недоступность Redis не роняет
приём: ``redis_ping`` возвращает False, обработка продолжается.
"""

from __future__ import annotations

import redis.asyncio as redis_async

from app.core.config import get_settings

_client: redis_async.Redis[str] | None = None


def get_redis() -> redis_async.Redis[str]:
    global _client
    if _client is None:
        _client = redis_async.from_url(
            get_settings().redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
    return _client


async def redis_ping() -> bool:
    try:
        return bool(await get_redis().ping())
    except Exception:
        return False


async def close_redis() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
    _client = None
