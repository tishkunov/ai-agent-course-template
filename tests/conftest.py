"""Фикстуры тестов M1.

- Юнит-тесты (`tests/unit/`) не зависят ни от одной фикстуры → БД не нужна.
- Интеграционные берут `client` / `session`; те тянут `_clean_db`, которому нужна
  отдельная тестовая БД Postgres. Схема применяется МИГРАЦИЯМИ (фикстура `_schema`),
  изоляция между тестами — TRUNCATE + рестарт последовательности после каждого.

ENV тестовой БД — из реального окружения (CI) или значений по умолчанию ниже
(локально: `docker compose -f docker/docker-compose.yml up -d postgres`).
"""

from __future__ import annotations

import os
from collections.abc import AsyncIterator, Iterator

import pytest
import pytest_asyncio
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

os.environ.setdefault("APP_ENV", "local")
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://intake:intake@localhost:5432/intake_test"
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/1")
os.environ.setdefault("JWT_SECRET", "test-secret-test-secret-test-secret-32")
os.environ.setdefault("JWT_TTL_MIN", "60")
os.environ.setdefault("API_KEYS", "test-key")
os.environ.setdefault("LOG_LEVEL", "WARNING")

from app.core.config import get_settings
from app.core.security import issue_operator_token
from app.db.session import dispose_engine
from app.main import create_app
from app.redis_client import close_redis


def _alembic_config() -> Config:
    cfg = Config("alembic.ini")
    cfg.set_main_option("script_location", "migrations")
    cfg.set_main_option("sqlalchemy.url", get_settings().database_url)
    return cfg


@pytest.fixture(scope="session")
def _schema() -> Iterator[None]:
    command.upgrade(_alembic_config(), "head")
    yield
    command.downgrade(_alembic_config(), "base")


@pytest_asyncio.fixture
async def _clean_db(_schema: None) -> AsyncIterator[None]:
    yield
    engine = create_async_engine(get_settings().database_url)
    async with engine.begin() as conn:
        await conn.execute(sa.text("TRUNCATE TABLE requests"))
        await conn.execute(sa.text("ALTER SEQUENCE request_seq RESTART WITH 1"))
    await engine.dispose()
    await dispose_engine()
    await close_redis()


@pytest_asyncio.fixture
async def session(_clean_db: None) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(get_settings().database_url)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    async with maker() as sess:
        yield sess
    await engine.dispose()


@pytest_asyncio.fixture
async def client(_clean_db: None) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as http:
        yield http


@pytest.fixture
def api_key_header() -> dict[str, str]:
    return {"X-API-Key": "test-key"}


@pytest.fixture
def operator_header() -> dict[str, str]:
    return {"Authorization": f"Bearer {issue_operator_token()}"}
