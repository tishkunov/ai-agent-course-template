# docs/_templates/ — болванки артефактов процесса

Здесь лежат пустые шаблоны всех документов, которые ведутся по ходу курса (`ai_context/4-process/12-process-raboty.md`, `ai_context/4-process/18-sdlc-pipeline.md`, `ai_context/5-instrumenty/19-rasshirennye-roli-agentov.md`).

## Как пользоваться

- При старте курса скопируй в `docs/` то, что ведётся постоянно:
  `working_agreement.md`, `decisions.md`, `progress.md`, `prompt_templates.md`.
- При работе над крупным пунктом/фичей копируй по мере надобности:
  `requirements.md` (агент `analyst`), `research-report.md` (`research`/`researcher`),
  `tech-design.md` (`design`/`designer`), `implementation-plan.md` (`plan`/`planner`),
  `plan-review.md` (агент `plan-reviewer`), `code-review.md` (`review`/`reviewer`),
  `test-report.md` (агент `tester`), `final-review.md` (агент `final-reviewer`),
  `bug-report.md` (агент `debugger`).
- Один активный документ на роль. Новый прогон той же роли перезаписывает файл в `docs/`
  (история решений остаётся в локальном `decisions.md`; рабочие записи не публикуются в Git).

## Правило

`_templates/` **не редактируется** по ходу работы — это эталон формата. Правки идут в копиях внутри `docs/`.
Если формат самого шаблона не подходит — это отдельное решение (запись в `decisions.md`), а не тихая правка болванки.

## Соответствие «фаза SDLC → шаблон → гейт»

| Фаза (`ai_context/4-process/18`) | Шаблон | Гейт после |
|---|---|---|
| 1. Требования | `requirements.md` | 🔴 требования одобрены |
| 2. Тех-дизайн | `tech-design.md` | 🟡 ключевые решения показаны |
| 3. Ревью дизайна | (вердикт READY/BLOCKED, встроенный `design-reviewer`) | 🔴 READY FOR PLANNING |
| 4. Планирование | `implementation-plan.md` | — |
| 5. Ревью плана | `plan-review.md` | 🔴 план одобрен |
| 6. Реализация | код + отметки в плане | 🟡 scope creep |
| 7. Финальное ревью | `code-review.md` + `test-report.md` + `/security-review` | 🔴 HIGH/CRITICAL |
| Приёмка модуля | `final-review.md` | 🔴 APPROVED |
