"""Pydantic-схемы границы API (M1.2). Схема ≠ ORM-модель: поля описаны отдельно,
ORM-типы не тянутся. ``extra="forbid"`` — неизвестное поле во входе → 422.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

RAW_TEXT_MAX = 20000


class Channel(StrEnum):
    email = "email"
    form = "form"
    messenger = "messenger"


class RequestCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: Channel
    raw_text: str = Field(min_length=1, max_length=RAW_TEXT_MAX)
    client_contact: str | None = Field(default=None, max_length=255)
    attachment_ref: str | None = Field(default=None, max_length=512)
    message_id: str | None = Field(default=None, max_length=255)

    @field_validator("raw_text")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("raw_text must not be blank")
        return value


class RequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: str
    created_at: datetime


class DepStatus(BaseModel):
    db: str
    redis: str


class HealthOut(BaseModel):
    status: str
    deps: DepStatus
    version: str
