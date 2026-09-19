"""Структурное JSON-логирование с correlation id (M1 §0).

Секреты и контактные данные не попадают в лог в открытом виде: поля с
чувствительными именами вырезаются из структурированной части записи.
"""

from __future__ import annotations

import json
import logging
import sys

_SENSITIVE_KEYS = frozenset(
    {
        "authorization",
        "x-api-key",
        "api_key",
        "api_keys",
        "jwt_secret",
        "password",
        "token",
        "secret",
    }
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, object] = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        request_id = getattr(record, "request_id", None)
        if request_id is not None:
            payload["request_id"] = request_id
        extra: dict[str, object] = getattr(record, "extra_fields", {})
        for key, value in extra.items():
            if key.lower() in _SENSITIVE_KEYS:
                continue
            payload[key] = value
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
