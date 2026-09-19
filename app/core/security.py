"""Аутентификация: приём — по API-ключу, операторские ручки — по JWT (M1.8).

Секрет из конфига (env). Алгоритм JWT зафиксирован в коде и не берётся из токена,
``alg=none`` и подмена алгоритма отбиваются. Ключи сравниваются постоянным временем.
"""

from __future__ import annotations

import hmac
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Header

from app.core.config import Settings, get_settings
from app.core.errors import Unauthorized

_ALGORITHM = "HS256"


def require_api_key(
    settings: Annotated[Settings, Depends(get_settings)],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> None:
    if x_api_key is None:
        raise Unauthorized("missing api key")
    if any(hmac.compare_digest(x_api_key, known) for known in settings.api_keys):
        return
    raise Unauthorized("invalid api key")


@dataclass(frozen=True)
class Operator:
    subject: str


def issue_operator_token(subject: str = "operator", *, settings: Settings | None = None) -> str:
    cfg = settings or get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "role": "operator",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=cfg.jwt_ttl_min)).timestamp()),
    }
    return jwt.encode(payload, cfg.jwt_secret, algorithm=_ALGORITHM)


def require_operator(
    settings: Annotated[Settings, Depends(get_settings)],
    authorization: Annotated[str | None, Header(alias="Authorization")] = None,
) -> Operator:
    if not authorization or not authorization.startswith("Bearer "):
        raise Unauthorized("missing bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[_ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
    except jwt.PyJWTError as exc:
        raise Unauthorized("invalid token") from exc
    subject = payload.get("sub")
    if not isinstance(subject, str) or not subject:
        raise Unauthorized("invalid token")
    return Operator(subject=subject)
