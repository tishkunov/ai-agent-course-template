"""Зависимости FastAPI: сессия БД и сервисы (M1.4)."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.services.intake import IntakeService
from app.services.read import RequestReadService

SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_intake_service(session: SessionDep) -> IntakeService:
    return IntakeService(session)


def get_read_service(session: SessionDep) -> RequestReadService:
    return RequestReadService(session)


IntakeServiceDep = Annotated[IntakeService, Depends(get_intake_service)]
ReadServiceDep = Annotated[RequestReadService, Depends(get_read_service)]
