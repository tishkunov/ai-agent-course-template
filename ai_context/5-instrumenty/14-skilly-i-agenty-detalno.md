# Каталог скиллов и агентов Claude Code (детально)

## 11. Каталог скиллов и агентов Claude Code (детально)

Короткая версия — `../00-navigatsiya.md` §0.2. Здесь — что каждый скилл делает, на каком шаге цикла и на каком модуле особенно нужен. Скиллы вызываются как `/<имя>`; агенты — через запуск сабагента с тем же именем.

### 11.1 Рабочий цикл проекта (сквозные, есть на каждом M)

| Скилл | Агент | Что делает | Шаг цикла M0.2 | Артефакт |
|---|---|---|---|---|
| `research` | `researcher` | анализ кодовой базы/подсистемы перед реализацией: структура, модели, потоки, слабые места | до шага 2 (разобраться) | `docs/research-report.md` |
| `design` | `designer` | тех-дизайн фичи: проблема, архитектура, диаграммы, модель данных, API-контракт, краевые случаи, открытые вопросы | до шага 2 для крупного пункта | `docs/tech-design.md` |
| `design-review` | `design-reviewer` | проверка тех-дизайна на полноту/прочность/безопасность до планирования | после `design` | вердикт + список по severity |
| `plan` | `planner` | разбивка фичи на маленькие поставляемые итерации: файлы, критерии готовности, оценки | после дизайна | `docs/implementation-plan.md` |
| `implement` | `implementer` | реализация ровно одной итерации/пункта — не больше и не меньше, отметка done в плане | шаг 3 (код) | код + правки плана |
| `review` | `reviewer` | ревью изменённых файлов в два прохода (качество + безопасность), замечания с `file:line`, черновик PR-описания | шаг 4 (обязательно отдельный вызов) | список замечаний + PR-описание |
| `/code-review` | — | ревью диффа / PR / ветки на баги и упрощения; уровни low→max; `--fix` применяет, `--comment` пишет в PR | шаг 4 (альтернатива/дополнение) | замечания |
| `/simplify` | — | только чистка: переиспользование, упрощение, эффективность; багов не ищет | после шага 4 | правки |
| `/security-review` | — | security-ревью изменений ветки | шаг 4 для M6.10, весь M7, M1.8 | отчёт |

Правило разделения (из M0.2): шаг 3 и шаг 4 — **разные вызовы**. Не просить `implement` тут же себя проверить. Полный чек-лист код-ревью под стек курса (что смотреть в SQLAlchemy/FastAPI/LangGraph/RAG-коде, severity, формат вывода) — `ai_context/3-priyomka/22-review-detalno.md`.

### 11.1a Проектные сабагенты (`.claude/agents/`)

Роли из SDLC-пайплайна (`../4-process/18-sdlc-pipeline.md`), для которых нет встроенного эквивалента, установлены как настоящие сабагенты — вызываются `Agent(subagent_type: "<имя>", ...)` наравне со встроенными. Полные системные промпты — в файлах, контракты — в `ai_context/5-instrumenty/19-rasshirennye-roli-agentov.md`. Поле `model` в них намеренно не задано — модель на выбор пользователя (ориентир — `ai_context/5-instrumenty/16-model-tiering.md`).

| Сабагент | Файл | Когда звать | Вход → Выход |
|---|---|---|---|
| `analyst` | `.claude/agents/analyst.md` | пункт/фича неоднозначны, до дизайна | запрос/пункт M.x → `docs/requirements.md` |
| `plan-reviewer` | `.claude/agents/plan-reviewer.md` | сразу после `planner`, до начала `implement` | `implementation-plan.md` → `docs/plan-review.md` (APPROVED/NEEDS_REVISION) |
| `tester` | `.claude/agents/tester.md` | пишет/аудирует тесты пункта или итерации (шаг 5 цикла) | код итерации → тесты + `docs/test-report.md` |
| `final-reviewer` | `.claude/agents/final-reviewer.md` | перед интеграционной приёмкой модуля | все доки + живой стек → `docs/final-review.md` |
| `debugger` | `.claude/agents/debugger.md` | сложный/интермиттентный баг, не пойманный тестами | репро/логи → `docs/bug-report.md` |

### 11.2 Проектирование и схемы

- **`artifact-diagramming`** — диаграммы в артефакте (Mermaid в ```` ```mermaid ````, либо инлайн-SVG). Здесь пригодится для: пайплайна S1–S10 (`../1-proekt/04-pipeline-s1-s10.md`), машины состояний обращения (`../1-proekt/03-statusy-i-perehody.md`), графа LangGraph (M6.4), последовательности до-сбора (M3), схемы RAG-конвейера (M5), архитектуры очередей (M8).
- **`dataviz`** — читать ПЕРЕД любым графиком/дашбордом. Модули: M4 (таблица сравнения эмбеддингов/классика-vs-LLM, per-class метрики), M7 (метрики eval, калибровка judge), M9 (дашборд: latency p95, ошибки, очередь, кеш, доля авто/эскалаций, стоимость/обращение), M8 (throughput/latency нагрузки).
- **`frontend-design`** + **`artifact-design`** + **`artifact-capabilities`** — экран оператора (M6.9, S10): очередь эскалаций, карточка обращения, кнопки подтвердить/править/отклонить. `artifact-capabilities` — если нужен сохраняемый стейт (чек-лист, форма).

### 11.3 Объяснение и обучение (главная цель курса)

- Раздел **«Понять»** каждого пункта в `course/M{n}-*/zadanie.md` — обязателен, закрывается пересказом в `docs/decisions.md`. ИИ объясняет концепцию, но финальную формулировку пишет пользователь (`../1-proekt/01-rol-assistenta.md`).
- **`research`** — когда нужно объяснить «как это уже устроено» в собранном коде.
- **`claude-api`** — справочник по LLM (id моделей семейства Claude, цены, параметры, стриминг, tool use, MCP, prompt caching, подсчёт токенов). Не отвечать по памяти на вопросы про модели/цены — читать этот скилл. Модули M2, M5, M6, M7, M8.
- Агент **`claude-code-guide`** — вопросы про сам Claude Code / Agent SDK / Anthropic API / хуки / слэш-команды / MCP-серверы.

### 11.4 Поднять и прогнать проект

- **`run`** — запустить приложение и убедиться, что изменение работает вживую (не только тесты); снять скриншот. Для M1 — `docker compose up`; дальше — тот же сервис.
- **`init`** — создать `CLAUDE.md` с описанием кодовой базы (полезно после M1, когда появился скелет).
- **`update-config`** — всё, что должно происходить автоматически: хуки (`после каждого пункта — ruff+mypy`, `перед коммитом — тесты`), права (`allow docker`, `allow alembic`), env. Автоповедение «каждый раз когда…» реализуется хуком в `settings.json`, не памятью.
- **`/fewer-permission-prompts`** — собрать allowlist частых безопасных команд, чтобы меньше подтверждать.
- **`claude-in-chrome`** — проверить `/docs` или экран оператора (M6.9) в реальном браузере, почитать консоль/сеть.

### 11.5 Автоматизация и утилиты

- **`/loop`** — повторять действие по интервалу: следить за нагрузочным прогоном M8, периодически гонять регресс-гейт M7.
- **`schedule`** — крон-агенты (routine) для регулярных проверок.
- **`/caveman`** — ультра-сжатый режим, когда сессия распухла.
- Сабагенты **`Explore`** (широкий поиск по файлам), **`Plan`** (архитектурный разбор без записи), **`general-purpose`** (многошаговый поиск/задача), **`fork`** (форк текущего контекста в фоне).

### 11.6 Быстрый маршрут по модулям

| M | Что поднять/прочитать до старта | Ключевые скиллы |
|---|---|---|
| M0 | `docs/working_agreement.md`, `docs/decisions.md`, `prompts/` | `update-config` (хуки цикла), `init` |
| M1 | Docker, Postgres, Redis; таблица стека `../2-po-modulyam/06-stek-po-modulyam.md` | `research`, `implement`, `review`, `run`, `/security-review` (M1.8), `artifact-diagramming` (машина состояний) |
| M2 | SDK провайдера или Ollama; таблица цен | `claude-api` (обязательно), `implement`, `review` |
| M3 | LLMClient из M2, таблица `messages` | `claude-api`, `artifact-diagramming` (ветки до-сбора) |
| M4 | sentence-transformers, scikit-learn; `data/course_pack/eval/classification_*` | `dataviz` (сравнение, per-class), `implement`, `review` |
| M5 | pgvector, парсеры docx/pdf, tesseract, реранкер; `data/course_pack/kb/`, `data/course_pack/inputs/rag.jsonl` | `research`, `design`, `artifact-diagramming` (RAG-конвейер), `dataviz` (faithfulness/recall@k) |
| M6 | LangGraph + Postgres saver, локальный MCP; `data/course_pack/reference/` инструменты | `design` + `design-review`, `plan`, `artifact-diagramming` (граф), `frontend-design` (экран оператора), `/security-review` (M6.10) |
| M7 | eval-раннер, judge через LLMClient; `data/course_pack/inputs/security.jsonl`, весь `data/course_pack/eval/` | `/security-review`, `claude-api` (judge), `dataviz`, `/loop` (регресс-гейт) |
| M8 | RabbitMQ/Redis Streams, breaker, Locust/k6; `data/course_pack/inputs/replay.jsonl` | `design`, `artifact-diagramming` (очереди), `/loop` (нагрузка), `dataviz` |
| M9 | Langfuse, Prometheus+Grafana | `dataviz` (дашборд — обязательно), `artifact-diagramming` |

---
