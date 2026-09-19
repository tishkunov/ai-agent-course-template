"""Чтение учебного course_pack: входы отдельно от эталонов."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parent


class DataSetError(RuntimeError):
    """Ошибка формата или целостности учебного пакета."""


def _require(path: Path) -> Path:
    if not path.is_file():
        raise DataSetError(f"Нет файла учебного пакета: {path}")
    return path


def _course_rows(task: str, directory: str, split: str | None, root: Path | None) -> list[dict[str, Any]]:
    """Read a manifest-listed task and verify its exported file before use."""
    import hashlib
    pack = Path(root) if root is not None else DATA_DIR / "course_pack"
    manifest = json.loads(_require(pack / "manifest.json").read_text(encoding="utf-8"))
    if task not in manifest["cases"]:
        raise DataSetError(f"Неизвестная задача course_pack: {task!r}")
    if split not in (None, "train", "dev", "test", "regression"):
        raise DataSetError(f"Неизвестный split: {split!r}")
    name = f"inputs/{task}.jsonl" if directory == "inputs" else "scenarios.jsonl"
    raw = _require(pack / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest["files"][name]:
        raise DataSetError(f"Хеш {name} не совпадает с manifest; проверьте версию данных")
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    return [r for r in rows if (directory == "inputs" or r["task"] == task)
            and (split is None or r["split"] == split)]


def load_course_inputs(task: str, *, split: str | None = None, root: Path | None = None) -> list[dict[str, Any]]:
    """Input envelopes without gold. Pass only task-authorized input fields to the model."""
    return _course_rows(task, "inputs", split, root)


def load_course_cases(task: str, *, split: str | None = None, root: Path | None = None) -> list[dict[str, Any]]:
    """Full cases with gold/evidence, exclusively for evaluation and test harnesses."""
    return _course_rows(task, "scenarios", split, root)
