"""M1.2 — правила валидации входа отбиваются на границе схемы."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.schemas.request import RequestCreate


def _valid() -> dict[str, object]:
    return {"channel": "form", "raw_text": "нужен электрик"}


def test_valid_body_parses() -> None:
    model = RequestCreate.model_validate(_valid())
    assert model.channel.value == "form"


def test_unknown_channel_rejected() -> None:
    with pytest.raises(ValidationError):
        RequestCreate.model_validate({**_valid(), "channel": "carrier-pigeon"})


def test_empty_raw_text_rejected() -> None:
    with pytest.raises(ValidationError):
        RequestCreate.model_validate({**_valid(), "raw_text": ""})


def test_blank_raw_text_rejected() -> None:
    with pytest.raises(ValidationError):
        RequestCreate.model_validate({**_valid(), "raw_text": "   "})


def test_too_long_raw_text_rejected() -> None:
    with pytest.raises(ValidationError):
        RequestCreate.model_validate({**_valid(), "raw_text": "x" * 20001})


def test_extra_field_rejected() -> None:
    with pytest.raises(ValidationError):
        RequestCreate.model_validate({**_valid(), "surprise": 1})
