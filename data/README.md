# Учебные данные

Единственный набор для M1–M9 — [course_pack](course_pack/README.md).
[Карта по модулям](../course/data-readiness.md) объясняет, какие задачи запускать;
[SCHEMA](SCHEMA.md) — как читать входы и эталоны.

```python
from data.loader import load_course_inputs, load_course_cases

inputs = load_course_inputs("classification", split="dev")
cases = load_course_cases("classification", split="dev")
```

В модель передавайте только разрешённые поля `input`. Эталоны нужны тестам и
самопроверке; `case_id`, `family_id`, `split`, `expected`, `basis` в промпт не входят.
Справочники лежат в `course_pack/reference/`, документы — в `course_pack/kb/`.
Форматы для упражнения ingestion — в `course_pack/fixtures/legacy_formats/`;
они изолированы от действующей базы знаний.

Намеренные конфликты документов, недоступные договоры, испорченные импорты и
security-входы — часть заданий. Manifest, scopes, версии и хеши нужны для
проверки доступа, актуальности и целостности; удалять их нельзя.
