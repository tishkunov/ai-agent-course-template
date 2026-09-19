# Стек и инструментарий по модулям

## 3. Инвентарь инструментария по модулям

Для ИИ-ассистента: не предлагай библиотеку/сервис, не входящие в этот список, без явного запроса пользователя — стек уже выбран по ТЗ.

| M | Стек/сервисы | Ключевые env/конфиг | Файлы-артефакты |
|---|---|---|---|
| M1 | Python 3.12, uv/poetry (lock в git), FastAPI, pydantic v2 + pydantic-settings, SQLAlchemy 2.0 async + asyncpg, Alembic, Redis (только подключение), Docker + docker-compose, JWT, ruff, mypy/pyright, pytest + httpx.AsyncClient | `APP_ENV, DATABASE_URL, REDIS_URL, JWT_SECRET, JWT_TTL_MIN, API_KEYS, LOG_LEVEL` | `app/{api,services,db,models,schemas,core}`, `migrations/`, `docker/`, `.env.example`, `Makefile` |
| M2 | SDK одного выбранного реального провайдера + тестовый адаптер, токенайзер модели | `LLM_PROVIDER, LLM_MODEL, LLM_API_KEY, LLM_BASE_URL/OLLAMA_URL, LLM_TIMEOUT` | `prompts/extract_v1.*`, таблица цен, миграция `llm_calls` |
| M3 | без нового внешнего сервиса — LLMClient (M2) + БД | `MAX_CLARIFY_ROUNDS` | `prompts/clarify_v1.*`, `prompts/summarize_v1.*`, таблица `messages` |
| M4 | sentence-transformers (эмбеддинги, CPU), простое голосование k=3 по ближайшим примерам; библиотека метрик при необходимости | seed, model/revision, база train-векторов, порог согласованности | база векторов и manifest, одна таблица majority/соседи/LLM |
| M5 | pgvector (расширение Postgres), парсеры docx/pdf (python-docx, pypdf/pdfplumber), tesseract OCR, cross-encoder реранкер (CPU) | размер/overlap чанка, top-k, вес гибрида (RRF), N для реранка | `kb_documents`, `kb_chunks`, `prompts/rag_answer_v1.*` |
| M6 | LangGraph (+ Postgres saver/checkpointer), MCP (локальный stdio-сервер) | лимит шагов графа, белый список инструментов | `agent_checkpoints`, `actions`, `escalations`, `tickets` |
| M7 | eval-раннер (pytest/скрипт), LLM-судья через LLMClient (M2) | пороги регресса, порог расхождения judge/разметка | `eval_runs` (или файлы), `prompts/judge_v1.*` |
| M8 | Redis Streams, circuit breaker (кастом/библиотека), Locust/k6 | таймауты/backoff по каждому внешнему вызову, бюджеты (`usage_counters`) | `processed_messages`, кеш (Redis/pgvector) |
| M9 | Langfuse (self-host docker или free cloud), Prometheus + Grafana (docker) | пороги алертов | дашборд, правила алертов |

Это карта будущих зависимостей. Перед модулем отличай уже существующее от того, что студент добавляет в текущем пункте; отсутствие будущей таблицы/конфига не означает неисправность каркаса. Точный объём — в задании. Второй адаптер не нужен M2; запасная модель остаётся обязательной в M8.

---
