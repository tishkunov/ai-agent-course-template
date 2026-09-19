"""M1.11 — /health различает критичную БД (503) и некритичный Redis (degraded/200)."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.api.routes import health as health_mod


async def _true() -> bool:
    return True


async def _false() -> bool:
    return False


async def test_health_ok_when_all_deps_up(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(health_mod, "_check_db", _true)
    monkeypatch.setattr(health_mod, "redis_ping", _true)
    resp = await client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["deps"] == {"db": "up", "redis": "up"}


async def test_health_503_when_db_down(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(health_mod, "_check_db", _false)
    monkeypatch.setattr(health_mod, "redis_ping", _true)
    resp = await client.get("/health")
    assert resp.status_code == 503
    assert resp.json()["status"] == "unhealthy"


async def test_health_degraded_when_only_redis_down(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(health_mod, "_check_db", _true)
    monkeypatch.setattr(health_mod, "redis_ping", _false)
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "degraded"
    assert resp.json()["deps"]["redis"] == "down"
