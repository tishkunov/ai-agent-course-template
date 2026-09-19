# Навигация: папки курса и скиллы

## 0. Навигация: папки курса и скиллы Claude Code

### 0.1 Где что лежит

| Что | Файл(ы) | Когда открывать |
|---|---|---|
| Общие правила сервиса | [course/contracts.md](../course/contracts.md) | при расхождении модульных формулировок |
| **Задание по пунктам** (что делать) | `course/M{n}-*/zadanie.md` | шаг 1–3 цикла: собрать промпт-контракт |
| **Критерии приёмки** (чем принимать) | `course/M{n}-*/kriterii-priyomki.md` | шаг 5 цикла + приёмка модуля |
| **Детальное ревью** (что ревьюить) | `course/M{n}-*/detalnoe-review.md` | шаг 4 цикла: отдельный ревью-вызов |
| Мастер-контекст курса | `ai_context/` — папки `1-proekt/` (что собираем), `2-po-modulyam/` (инвентари: стек/данные/режимы ИИ), `3-priyomka/` (чем принимать и что ревьюить), `4-process/` (цикл, гейты, паттерны), `5-instrumenty/` (скиллы/агенты/модели Claude Code). Индекс — `ai_context/README.md` | держать открытым |
| Синтетические данные | `data/` (`reference/ requests/ dialogs/ eval/ knowledge_base/ security/ bulk/ feedback/ misc/`) | см. `2-po-modulyam/07-sinteticheskie-dannye.md` и `data/README.md` |
| Решения и промпты (ведёт пользователь) | `docs/decisions.md`, `docs/progress.md`, `prompts/<step>_v<N>.md` | каждый пункт (создаются по ходу курса) |

`course/M{n}-*/` содержит задание, проверку, риски отдельного ревью и пояснения. Их назначение и приоритет — в [технической карте](../course/README.md). Процесс M0 сохраняется; контекст ассистента не добавляет скрытых обязательств.

### 0.2 Скиллы и агенты Claude Code под этот курс (полный каталог — `5-instrumenty/14-skilly-i-agenty-detalno.md`)

| Задача | Скилл / агент | Артефакт |
|---|---|---|
| Понять кодовую базу / концепцию перед работой | `research` (или агент `researcher`) | `docs/research-report.md` |
| Спроектировать модуль/фичу | `design` → `designer` | `docs/tech-design.md` |
| Проверить дизайн до плана | `design-review` → `design-reviewer` | вердикт READY FOR PLANNING |
| Разбить на итерации | `plan` → `planner` | `docs/implementation-plan.md` |
| Написать код пункта M.x | `implement` → `implementer` | код + отметка в плане |
| Отдельный ревью-вызов (шаг 4 цикла) | `review` → `reviewer`, плюс `/code-review` | список замечаний + PR-описание |
| Аудит плана до реализации | сабагент `plan-reviewer` (`.claude/agents/`) | `docs/plan-review.md` |
| Написать/проверить тесты пункта (шаг 5) | сабагент `tester` (`.claude/agents/`) | тесты + `docs/test-report.md` |
| Неоднозначный запрос → требования | сабагент `analyst` (`.claude/agents/`) | `docs/requirements.md` |
| Холистическая приёмка перед закрытием модуля | сабагент `final-reviewer` (`.claude/agents/`) | `docs/final-review.md` |
| Сложный/интермиттентный баг | сабагент `debugger` (`.claude/agents/`) | `docs/bug-report.md` |
| Чистка кода без охоты за багами | `/simplify` | правки в рабочем дереве |
| Безопасность (обязательно в M6.10, M7) | `/security-review` | отчёт по уязвимостям ветки |
| Поднять / запустить приложение, снять скриншот | `run` | подтверждение, что работает вживую |
| Завести `CLAUDE.md` проекта | `init` | `CLAUDE.md` |
| Схемы и диаграммы (пайплайн S1–S10, граф M6, машина состояний) | `artifact-diagramming` (Mermaid/SVG в артефакте) | диаграмма-артефакт |
| Дашборды и графики метрик (M9), сравнение моделей (M4) | `dataviz` | графики/дашборд |
| Экран оператора (M6.9), любой UI | `frontend-design`, `artifact-design`, `artifact-capabilities` | UI-артефакт |
| Всё про LLM: id моделей, цены, токены, tool use, caching, MCP (M2, M5, M6, M7, M8) | `claude-api` | — (справка, не угадывать по памяти) |
| Проверить UI/HTTP в реальном браузере | `claude-in-chrome` | скриншоты, логи консоли |
| Вопросы «умеет ли Claude Code…», хуки, MCP, слэш-команды | агент `claude-code-guide` | ответ |
| Хуки / права / env в `settings.json` (например «после каждого пункта прогонять ruff») | `update-config` | правки `settings.json` |
| Меньше запросов на подтверждение | `/fewer-permission-prompts` | allowlist в `.claude/settings.json` |
| Повторяющаяся проверка по интервалу (следить за нагрузочным прогоном M8) | `/loop` | — |
| Расписание/крон-агент | `schedule` | routine |
| Резать токены в длинной сессии | `/caveman` | — |

Правило: **не подменяй цикл M0.2 скиллами.** Скилл `implement` = шаг 3 (код). Скилл `review` / `/code-review` = шаг 4, и он обязан быть ОТДЕЛЬНЫМ вызовом. «Понять» (шаг 6) не закрывается ни одним скиллом — только пересказом пользователя в `docs/decisions.md`.

---
