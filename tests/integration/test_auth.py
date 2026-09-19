"""M1.8 — матрица аутентификации: API-ключ на приёме, JWT на операторских ручках."""

from __future__ import annotations

import datetime as dt

import jwt
from httpx import AsyncClient

from app.core.config import get_settings
from app.core.security import issue_operator_token

PAYLOAD: dict[str, object] = {"channel": "form", "raw_text": "тест авторизации"}


async def test_intake_without_key_401(client: AsyncClient) -> None:
    assert (await client.post("/requests", json=PAYLOAD)).status_code == 401


async def test_intake_with_bad_key_401(client: AsyncClient) -> None:
    resp = await client.post("/requests", json=PAYLOAD, headers={"X-API-Key": "nope"})
    assert resp.status_code == 401


async def test_intake_with_valid_key_201(
    client: AsyncClient, api_key_header: dict[str, str]
) -> None:
    resp = await client.post("/requests", json=PAYLOAD, headers=api_key_header)
    assert resp.status_code == 201


async def test_get_request_requires_operator_jwt(
    client: AsyncClient, api_key_header: dict[str, str]
) -> None:
    created = await client.post("/requests", json=PAYLOAD, headers=api_key_header)
    request_id = created.json()["id"]

    assert (await client.get(f"/requests/{request_id}")).status_code == 401

    ok = await client.get(
        f"/requests/{request_id}",
        headers={"Authorization": f"Bearer {issue_operator_token()}"},
    )
    assert ok.status_code == 200
    assert ok.json()["id"] == request_id


async def test_expired_token_401(client: AsyncClient) -> None:
    settings = get_settings()
    expired = jwt.encode(
        {
            "sub": "operator",
            "exp": int((dt.datetime.now(dt.UTC) - dt.timedelta(minutes=1)).timestamp()),
        },
        settings.jwt_secret,
        algorithm="HS256",
    )
    resp = await client.get(
        "/requests/REQ-2026-0001", headers={"Authorization": f"Bearer {expired}"}
    )
    assert resp.status_code == 401


async def test_alg_none_rejected(client: AsyncClient) -> None:
    forged = jwt.encode({"sub": "operator", "exp": 9999999999}, key="", algorithm="none")
    resp = await client.get(
        "/requests/REQ-2026-0001", headers={"Authorization": f"Bearer {forged}"}
    )
    assert resp.status_code == 401


async def test_wrong_secret_rejected(client: AsyncClient) -> None:
    forged = jwt.encode(
        {"sub": "operator", "exp": 9999999999}, "not-the-real-secret", algorithm="HS256"
    )
    resp = await client.get(
        "/requests/REQ-2026-0001", headers={"Authorization": f"Bearer {forged}"}
    )
    assert resp.status_code == 401
