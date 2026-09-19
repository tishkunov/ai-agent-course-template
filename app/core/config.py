"""Конфиг сервиса. Единственный источник — окружение / .env (M1.1).

Обязательные переменные не имеют дефолтов; их отсутствие → падение на старте
с понятным сообщением. Читается один раз через кешируемый геттер.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: Literal["local", "dev", "prod"] = Field(default="local", alias="APP_ENV")
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(alias="REDIS_URL")
    jwt_secret: str = Field(alias="JWT_SECRET", min_length=1)
    jwt_ttl_min: int = Field(default=60, alias="JWT_TTL_MIN", ge=1)
    # Хранится строкой ("key1,key2") — это обходит JSON-декодирование сложных
    # типов в pydantic-settings и работает на всех его версиях. Список — через
    # свойство ``api_keys``.
    api_keys_raw: str = Field(alias="API_KEYS")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", alias="LOG_LEVEL"
    )
    db_pool_size: int = Field(default=5, alias="DB_POOL_SIZE", ge=1)
    db_max_overflow: int = Field(default=10, alias="DB_MAX_OVERFLOW", ge=0)

    @field_validator("api_keys_raw")
    @classmethod
    def _has_api_key(cls, value: str) -> str:
        if not [item for item in value.split(",") if item.strip()]:
            raise ValueError("API_KEYS must contain at least one key")
        return value

    @property
    def api_keys(self) -> tuple[str, ...]:
        return tuple(item.strip() for item in self.api_keys_raw.split(",") if item.strip())

    @property
    def is_prod(self) -> bool:
        return self.app_env == "prod"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        # значения приходят из окружения/.env, не из аргументов вызова
        return Settings()  # type: ignore[call-arg]
    except ValidationError as exc:
        missing = ", ".join(
            ".".join(str(p) for p in err["loc"]) for err in exc.errors() if err["type"] == "missing"
        )
        hint = f" Отсутствуют обязательные переменные: {missing}." if missing else ""
        raise RuntimeError(f"Некорректная конфигурация окружения.{hint}") from exc
