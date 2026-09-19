"""Модель «Обращение» (таблица ``requests``).

Форма зафиксирована в M1.5 и в ai_context/11-stabilnye-kontrakty.md — таблица
растёт в следующих модулях только через миграции, поля не переименовываются.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Index, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

STATUS_NEW = "new"
ID_MAX_LEN = 32


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[str] = mapped_column(String(ID_MAX_LEN), primary_key=True)
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    thread_key: Mapped[str] = mapped_column(String(255), nullable=False)
    idem_key: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default=STATUS_NEW)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    client_contact: Mapped[str | None] = mapped_column(String(255), nullable=True)
    client_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    attachment_ref: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        UniqueConstraint("idem_key", name="uq_requests_idem_key"),
        Index("ix_requests_thread_key", "thread_key"),
        Index("ix_requests_status", "status"),
        Index("ix_requests_created_at", "created_at"),
    )
