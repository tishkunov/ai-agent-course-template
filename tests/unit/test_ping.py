"""M0.5 — тренировочный прогон цикла: ``/ping`` отдаёт 200 и обещанную форму.

Тест проверяет контракт из prompts/ping_v1.md (код 200 + три поля с их типами),
не реализацию. БД/Redis/auth не трогает — эндпоинт вне пайплайна проекта, поэтому
живёт в tests/unit/ и не зависит ни от одной фикстуры.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from httpx import ASGITransport, AsyncClient

from app.main import create_app


async def _get_ping() -> tuple[int, dict[str, object]]:
    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as http:
        resp = await http.get("/ping")
    return resp.status_code, resp.json()


async def test_ping_returns_200() -> None:
    status_code, _ = await _get_ping()
    assert status_code == 200


async def test_ping_response_shape() -> None:
    _, body = await _get_ping()

    assert set(body) == {"status", "version", "ts"}
    assert body["status"] == "ok"
    assert isinstance(body["version"], str) and body["version"]

    ts = body["ts"]
    assert isinstance(ts, str)
    parsed = datetime.fromisoformat(ts)  # валидный ISO-8601
    assert parsed.tzinfo is not None  # не наивный
    assert parsed.utcoffset() == timedelta(0)  # именно UTC (Требование 5), не любой tz
