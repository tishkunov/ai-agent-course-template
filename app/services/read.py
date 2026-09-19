"""Чтение обращения. Роут делегирует сюда, а не ходит в репозиторий напрямую (M1.4)."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFound
from app.db.repositories.request_repo import RequestRepository
from app.models.request import Request


class RequestReadService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = RequestRepository(session)

    async def get(self, request_id: str) -> Request:
        obj = await self._repo.get_by_id(request_id)
        if obj is None:
            raise NotFound("request not found")
        return obj
