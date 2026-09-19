"""Регистрация ORM-моделей в ``Base.metadata`` (импортируется alembic env.py)."""

from __future__ import annotations

from app.models.request import Request

__all__ = ["Request"]
