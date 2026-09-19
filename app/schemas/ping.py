"""Схема ответа тренировочного ``/ping`` (M0.5).

Ответ типизирован pydantic-схемой и не собирается «руками» из ``dict``
(prompts/ping_v1.md, блок «Контракты»).
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class PingOut(BaseModel):
    # Контракт M0.5 фиксирует значение, а не просто тип: {status: "ok"}.
    # Literal форсит его на уровне схемы, а не оставляет на совести теста.
    status: Literal["ok"]
    version: str
    ts: datetime
