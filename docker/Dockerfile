# syntax=docker/dockerfile:1
# Multi-stage: финальный образ slim, без dev-зависимостей и компилятора, запуск от non-root.
# Секретов в образ не кладём — они приходят из окружения в docker-compose / secret manager.

FROM python:3.12-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /bin/uv
WORKDIR /app
COPY pyproject.toml ./
# uv.lock ещё не закоммичен в шаблоне — добавь его и флаг --frozen для воспроизводимости.
COPY uv.loc[k] ./
RUN uv sync --no-dev --no-install-project
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini ./

FROM python:3.12-slim AS runtime
RUN useradd --create-home --uid 1000 appuser
WORKDIR /app
COPY --from=builder --chown=appuser:appuser /app /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
USER appuser
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
