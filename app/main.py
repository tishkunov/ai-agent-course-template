"""Сборка приложения (app factory) + middleware request_id + graceful shutdown (M1.4, M1.11)."""

from __future__ import annotations

import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response

from app.api.routes import health as health_routes
from app.api.routes import ping as ping_routes
from app.api.routes import requests as request_routes
from app.core.config import get_settings
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.db.session import dispose_engine
from app.redis_client import close_redis

VERSION = "0.1.0"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging(get_settings().log_level)
    yield
    await dispose_engine()
    await close_redis()


def create_app() -> FastAPI:
    app = FastAPI(title="Intake Agent", version=VERSION, lifespan=lifespan)

    @app.middleware("http")
    async def _request_id(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    register_error_handlers(app)
    app.include_router(request_routes.router)
    app.include_router(health_routes.router)
    app.include_router(ping_routes.router)
    return app


app = create_app()
