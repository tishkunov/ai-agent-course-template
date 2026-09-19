"""Приём обращения с идемпотентностью (M1.7 = S1, начало).

thread_key = ``channel:(contact|anon)``. idem_key:
- есть ``message_id`` → ``channel:message_id``;
- иначе → хеш ``channel|contact|нормализованный_text|date-bucket``.

Гонка двух одинаковых запросов ловится уникальным индексом ``uq_requests_idem_key``:
проигравший получает IntegrityError, читает существующую запись и отдаёт её (не 500).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.request_repo import RequestRepository
from app.models.request import Request
from app.schemas.request import RequestCreate


@dataclass(frozen=True)
class IntakeResult:
    request: Request
    is_new: bool


def _normalize_text(value: str) -> str:
    return " ".join(value.split()).lower()


def build_thread_key(channel: str, client_contact: str | None) -> str:
    return f"{channel}:{client_contact or 'anon'}"


def build_idem_key(payload: RequestCreate) -> str:
    channel = payload.channel.value
    if payload.message_id:
        return f"{channel}:{payload.message_id}"

    # DECISION NEEDED — зафиксировать в docs/decisions.md.
    # ТЗ M1.7 задаёт дедуп "в окне TTL (сутки)", но UNIQUE-индекс на idem_key
    # не имеет TTL: без ограничителя легитимный повтор той же заявки на
    # следующий день упрётся в конфликт. Здесь ВРЕМЕННО добавлен date-bucket
    # по UTC-дате. Альтернативы:
    #   (a) date-bucket в ключе  — текущее, простое, но граница суток резкая;
    #   (b) отдельная таблица дедупа с TTL и фоновой очисткой;
    #   (c) TTL на стороне приложения (Redis) + не-unique idem_key.
    bucket = datetime.now(UTC).strftime("%Y-%m-%d")
    contact = payload.client_contact or "anon"
    raw = f"{channel}|{contact}|{_normalize_text(payload.raw_text)}|{bucket}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return f"{channel}:hash:{digest}"


class IntakeService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = RequestRepository(session)

    async def accept(self, payload: RequestCreate) -> IntakeResult:
        idem_key = build_idem_key(payload)

        existing = await self._repo.get_by_idem_key(idem_key)
        if existing is not None:
            return IntakeResult(request=existing, is_new=False)

        thread_key = build_thread_key(payload.channel.value, payload.client_contact)
        try:
            created = await self._repo.create(
                channel=payload.channel.value,
                thread_key=thread_key,
                idem_key=idem_key,
                raw_text=payload.raw_text,
                client_contact=payload.client_contact,
                attachment_ref=payload.attachment_ref,
            )
        except IntegrityError:
            await self._session.rollback()
            racer = await self._repo.get_by_idem_key(idem_key)
            if racer is None:
                raise
            return IntakeResult(request=racer, is_new=False)
        return IntakeResult(request=created, is_new=True)
