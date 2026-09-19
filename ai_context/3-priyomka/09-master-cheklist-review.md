# Навигация отдельного ревью по модулям

На шаге 4 M0 выбирай `detalnoe-review.md` своего модуля. Это карта рисков, а не вторая копия
требований. Поведение задаёт `zadanie.md`, наблюдаемую проверку — `kriterii-priyomki.md`,
общую политику — [contracts](../../course/contracts.md). Обнаруженное расхождение исправляется
у владельца требования, а не скрывается новой локальной формулировкой.

| Модуль | Риск, на который обратить внимание | Проверки |
|---|---|---|
| [M1 ревью](../../course/M1-backend-fundament/detalnoe-review.md) | Существующий каркас, транзакции, конкурентный повтор, полномочия JWT, запуск без Redis | [приёмка](../../course/M1-backend-fundament/kriterii-priyomki.md) |
| [M2 ревью](../../course/M2-llm-osnovy/detalnoe-review.md) | Валидация фактов, ограниченный повтор, отдельный call_id на вызов, сохранение usage и неизвестной стоимости | [приёмка](../../course/M2-llm-osnovy/kriterii-priyomki.md) |
| [M3 ревью](../../course/M3-kontekst/detalnoe-review.md) | Идентичность диалога, durable история, merge исправлений, атомарность вопроса и счётчика | [приёмка](../../course/M3-kontekst/kriterii-priyomki.md) |
| [M4 ревью](../../course/M4-ml-minimum/detalnoe-review.md) | Эвристика соседей, отдельный приоритет, отказ после LLM, неполная независимость test | [приёмка](../../course/M4-ml-minimum/kriterii-priyomki.md) |
| [M5 ревью](../../course/M5-rag/detalnoe-review.md) | Допуск документов и scope, действующая версия, SQL vs RAG, неполная разметка источников | [приёмка](../../course/M5-rag/kriterii-priyomki.md) |
| [M6 ревью](../../course/M6-agenty/detalnoe-review.md) | Границы tool loop, события/паузы, права оператора, идентичность и восстановление действий | [приёмка](../../course/M6-agenty/kriterii-priyomki.md) |
| [M7 ревью](../../course/M7-ocenka-bezopasnost/detalnoe-review.md) | Реальные предсказания отдельно от mock, запрещённые эффекты, ложные отказы, неполный прогон | [приёмка](../../course/M7-ocenka-bezopasnost/kriterii-priyomki.md) |
| [M8 ревью](../../course/M8-nagruzka-stoimost/detalnoe-review.md) | Стабильный event_id, ack пауз, отказ публикации, права кеша, расходы всех вызовов | [приёмка](../../course/M8-nagruzka-stoimost/kriterii-priyomki.md) |
| [M9 ревью](../../course/M9-nablyudaemost/detalnoe-review.md) | Несколько запусков обращения, знаменатели метрик, PII, единый источник расходов, best-effort | [приёмка](../../course/M9-nablyudaemost/kriterii-priyomki.md) |

Критичные инварианты доступа M5.10/M6.10/M7, идемпотентность приёма M1.7 и действий M6.8,
исключение решений заявки из кеша M8.6 не откладываются как оптимизации. Не добавляй в ревью
задачи, которых нет в задании. Процесс M0 и его отдельный ревью-вызов сохраняются.
