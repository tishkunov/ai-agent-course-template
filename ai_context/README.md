# ai_context/ — мастер-контекст курса по кускам

Единый справочный документ на весь курс (M0–M9): что за проект собирается, какой стек/данные/скиллы нужны на каждом этапе, чем проверяется качество. Использовать как вспомогательный контекст. Приоритет: [общие контракты](../course/contracts.md) → задание модуля → его приёмка; details объясняют требования. Этот каталог не переопределяет задания.

**Главная цель курса — не «сдать модули», а быстро научиться собирать такой сервис с ИИ.** Поэтому у каждого пункта есть раздел «Понять» (закрывается пересказом своими словами), а весь материал разложен по папкам так, чтобы «что делать», «чем принимать» и «что ревьюить» не смешивались.

Файлы держат числовой префикс (`01`–`22`) — он задаёт исторический порядок; папка говорит, *зачем* файл открывают. Правятся напрямую.

---

## Старт

| Файл | О чём |
|---|---|
| [`00-navigatsiya.md`](00-navigatsiya.md) | Навигация: папки курса, где что лежит, каталог скиллов Claude Code |

## `1-proekt/` — что собираем (неизменное описание системы)

| Файл | О чём |
|---|---|
| [`1-proekt/01-rol-assistenta.md`](1-proekt/01-rol-assistenta.md) | Роль ассистента |
| [`1-proekt/02-proekt-obzor.md`](1-proekt/02-proekt-obzor.md) | Проект: обзор и сущности |
| [`1-proekt/03-statusy-i-perehody.md`](1-proekt/03-statusy-i-perehody.md) | Статусы и переходы обращения |
| [`1-proekt/04-pipeline-s1-s10.md`](1-proekt/04-pipeline-s1-s10.md) | Пайплайн S1–S10 |
| [`1-proekt/05-karta-moduley.md`](1-proekt/05-karta-moduley.md) | Карта модулей M0–M9 |

## `2-po-modulyam/` — что нужно на каждом M (инвентари)

| Файл | О чём |
|---|---|
| [`2-po-modulyam/06-stek-po-modulyam.md`](2-po-modulyam/06-stek-po-modulyam.md) | Стек и инструментарий по модулям |
| [`2-po-modulyam/07-sinteticheskie-dannye.md`](2-po-modulyam/07-sinteticheskie-dannye.md) | Синтетические данные по модулям |
| [`2-po-modulyam/08-rezhimy-ii-po-modulyam.md`](2-po-modulyam/08-rezhimy-ii-po-modulyam.md) | Режимы работы ИИ по модулям |

## `3-priyomka/` — чем принимать и что ревьюить

| Файл | О чём |
|---|---|
| [`3-priyomka/09-master-cheklist-review.md`](3-priyomka/09-master-cheklist-review.md) | Мастер-чек-лист ревью (по модулям) |
| [`3-priyomka/10-kriterii-kachestva.md`](3-priyomka/10-kriterii-kachestva.md) | Критерии качества: DoD, пороги, рубрика |
| [`3-priyomka/11-stabilnye-kontrakty.md`](3-priyomka/11-stabilnye-kontrakty.md) | Стабильные контракты курса |
| [`3-priyomka/22-review-detalno.md`](3-priyomka/22-review-detalno.md) | Детальный чек-лист код-ревью под стек курса |

## `4-process/` — как вести работу (цикл, гейты, паттерны)

| Файл | О чём |
|---|---|
| [`4-process/12-process-raboty.md`](4-process/12-process-raboty.md) | Процесс работы (памятка дня) |
| [`4-process/13-treker-progressa.md`](4-process/13-treker-progressa.md) | Трекер прогресса (шаблон) |
| [`4-process/15-human-gates.md`](4-process/15-human-gates.md) | Человеческие гейты одобрения 🔴/🟡/🟢 |
| [`4-process/17-orchestrator-workers.md`](4-process/17-orchestrator-workers.md) | Паттерн «Оркестратор + воркеры», Worker Brief |
| [`4-process/18-sdlc-pipeline.md`](4-process/18-sdlc-pipeline.md) | SDLC-пайплайн: 7 фаз с гейтами |
| [`4-process/20-pleybuki.md`](4-process/20-pleybuki.md) | Плейбуки: bug-hunt / refactor / perf-audit / db-migration / full-verify |
| [`4-process/21-core-principles.md`](4-process/21-core-principles.md) | Базовые принципы процесса + .claudeignore |

## `5-instrumenty/` — инструментарий Claude Code (скиллы, агенты, модели)

| Файл | О чём |
|---|---|
| [`5-instrumenty/14-skilly-i-agenty-detalno.md`](5-instrumenty/14-skilly-i-agenty-detalno.md) | Каталог скиллов и агентов Claude Code (детально) |
| [`5-instrumenty/16-model-tiering.md`](5-instrumenty/16-model-tiering.md) | Выбор модели (ориентир, не правило — модель на выбор пользователя) |
| [`5-instrumenty/19-rasshirennye-roli-agentov.md`](5-instrumenty/19-rasshirennye-roli-agentov.md) | Реестр ролей + стратегия привязки + контракты сабагентов |

---

Читается вместе с `course/M{n}-*/` (задание / приёмка / ревью по модулям) и общими правилами `course/contracts.md`.
