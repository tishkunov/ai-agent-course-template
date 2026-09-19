"""Тренировочный эндпоинт M0.5 (course/M0-start/M0TZstart.md, prompts/ping_v1.md).

Вне пайплайна проекта S1–S10 — это прогон цикла M0.2, не рабочая ручка. Намеренно
ничего не знает про БД, Redis, auth и слой ``services/``: версия берётся из
локальной константы модуля, ответ типизирован схемой.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter

from app.schemas.ping import PingOut

router = APIRouter(tags=["ping"])

# Единственный источник версии для этого эндпоинта (prompts/ping_v1.md, требование 4).
# M0.5 не трогает M1-файлы, поэтому VERSION из app.main здесь не переиспользуется.
VERSION = "0.1.0"


@router.get("/ping", response_model=PingOut)
async def ping() -> PingOut:
    return PingOut(status="ok", version=VERSION, ts=datetime.now(UTC))
