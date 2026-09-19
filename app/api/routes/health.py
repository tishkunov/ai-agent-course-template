"""Healthcheck (M1.11). db — критична (503), redis — нет (degraded/200).

Реально проверяет соединения, а не отдаёт заглушку ``ok``.
"""

from __future__ import annotations

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.db.session import get_sessionmaker
from app.redis_client import redis_ping
from app.schemas.request import DepStatus, HealthOut

router = APIRouter(tags=["health"])

VERSION = "0.1.0"


async def _check_db() -> bool:
    try:
        sessionmaker = get_sessionmaker()
        async with sessionmaker() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


@router.get("/health", response_model=HealthOut)
async def health(response: Response) -> HealthOut:
    db_ok = await _check_db()
    redis_ok = await redis_ping()

    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        overall = "unhealthy"
    elif not redis_ok:
        response.status_code = status.HTTP_200_OK
        overall = "degraded"
    else:
        overall = "ok"

    return HealthOut(
        status=overall,
        deps=DepStatus(
            db="up" if db_ok else "down",
            redis="up" if redis_ok else "down",
        ),
        version=VERSION,
    )
