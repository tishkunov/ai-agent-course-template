"""M1.7 — приём и идемпотентность (реальная тестовая БД, httpx.AsyncClient)."""

from __future__ import annotations

import asyncio

from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import Request

PAYLOAD: dict[str, object] = {
    "channel": "form",
    "raw_text": "нужен сантехник на завтра утром",
    "client_contact": "u@example.com",
}


async def test_create_returns_201_and_persists_new(
    client: AsyncClient, session: AsyncSession, api_key_header: dict[str, str]
) -> None:
    resp = await client.post("/requests", json=PAYLOAD, headers=api_key_header)
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "new"

    row = await session.get(Request, body["id"])
    assert row is not None
    assert row.status == "new"
    assert row.thread_key == "form:u@example.com"


async def test_repeat_returns_200_same_id_no_second_row(
    client: AsyncClient, session: AsyncSession, api_key_header: dict[str, str]
) -> None:
    first = await client.post("/requests", json=PAYLOAD, headers=api_key_header)
    second = await client.post("/requests", json=PAYLOAD, headers=api_key_header)

    assert first.status_code == 201
    assert second.status_code == 200
    assert first.json()["id"] == second.json()["id"]

    count = await session.scalar(select(func.count()).select_from(Request))
    assert count == 1


async def test_concurrent_duplicates_create_single_row(
    client: AsyncClient, session: AsyncSession, api_key_header: dict[str, str]
) -> None:
    results = await asyncio.gather(
        *(client.post("/requests", json=PAYLOAD, headers=api_key_header) for _ in range(8))
    )
    assert all(r.status_code in (200, 201) for r in results)
    assert len({r.json()["id"] for r in results}) == 1

    count = await session.scalar(select(func.count()).select_from(Request))
    assert count == 1


async def test_message_id_makes_idempotency_key(
    client: AsyncClient, session: AsyncSession, api_key_header: dict[str, str]
) -> None:
    payload = {"channel": "email", "raw_text": "любой текст", "message_id": "<abc@mail>"}
    a = await client.post("/requests", json=payload, headers=api_key_header)
    payload_other_text = {**payload, "raw_text": "совсем другой текст"}
    b = await client.post("/requests", json=payload_other_text, headers=api_key_header)

    assert a.status_code == 201
    assert b.status_code == 200
    assert a.json()["id"] == b.json()["id"]
    count = await session.scalar(select(func.count()).select_from(Request))
    assert count == 1


async def test_invalid_body_maps_to_422(
    client: AsyncClient, api_key_header: dict[str, str]
) -> None:
    resp = await client.post("/requests", json={"channel": "form"}, headers=api_key_header)
    assert resp.status_code == 422
    assert resp.json()["error"] == "validation_failed"


async def test_missing_api_key_is_401(client: AsyncClient) -> None:
    resp = await client.post("/requests", json=PAYLOAD)
    assert resp.status_code == 401
