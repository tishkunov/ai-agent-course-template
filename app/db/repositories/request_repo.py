"""Слой доступа к ``requests`` (M1.5). Никакого сырого SQL из конкатенации.

Бизнес-ключ ``REQ-YYYY-NNNN`` генерируется в одном месте — через Postgres-
последовательность ``request_seq`` (создаётся миграцией 0001).
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import STATUS_NEW, Request


class RequestRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _next_id(self) -> str:
        result = await self._session.execute(text("SELECT nextval('request_seq')"))
        seq = int(result.scalar_one())
        return f"REQ-{datetime.now(UTC).year}-{seq:04d}"

    async def create(
        self,
        *,
        channel: str,
        thread_key: str,
        idem_key: str,
        raw_text: str,
        client_contact: str | None,
        attachment_ref: str | None,
    ) -> Request:
        obj = Request(
            id=await self._next_id(),
            channel=channel,
            thread_key=thread_key,
            idem_key=idem_key,
            status=STATUS_NEW,
            raw_text=raw_text,
            client_contact=client_contact,
            attachment_ref=attachment_ref,
        )
        self._session.add(obj)
        await self._session.flush()
        return obj

    async def get_by_id(self, request_id: str) -> Request | None:
        return await self._session.get(Request, request_id)

    async def get_by_idem_key(self, idem_key: str) -> Request | None:
        result = await self._session.execute(select(Request).where(Request.idem_key == idem_key))
        return result.scalar_one_or_none()
