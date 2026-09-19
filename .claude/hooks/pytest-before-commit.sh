#!/usr/bin/env bash
# PreToolUse(Bash)-хук. Поле "if": "Bash(git commit:*)" в settings.json — грубый
# префиксный фильтр: он НЕ держится для команд с ведущим присваиванием
# (`VAR=x git commit ...`) и для составных (`cd d && git commit`). Поэтому здесь
# есть собственный guard по фактическому тексту команды из stdin.
#
# Смысл: перед `git commit` прогнать тесты; провал блокирует коммит
# (ai_context/21, принцип №6: «Тесты — гейты качества, красные блокируют merge»).
#
# Коды выхода: 0 — пропустить; 2 — блокирующая ошибка (коммит отменяется).
set -uo pipefail

payload="$(cat)"

cmd="$(printf '%s' "$payload" | python3 -c 'import sys,json
try:
    d = json.load(sys.stdin)
except Exception:
    print(""); sys.exit(0)
print(d.get("tool_input", {}).get("command", ""))' 2>/dev/null || true)"

# Guard: реагируем только на реальный `git commit`, не на `git commit-graph`,
# не на `git log`, не на упоминание в строке.
case "$cmd" in
  *"git commit"|*"git commit "*) ;;
  *) exit 0 ;;
esac

# Выбираем pytest из окружения проекта, а не системный (у системного не будет
# зависимостей → conftest не соберётся → ложный блок).
if [ -x ".venv/bin/pytest" ]; then
  runner=(.venv/bin/pytest -q)
elif command -v uv >/dev/null 2>&1 && [ -f "pyproject.toml" ]; then
  runner=(uv run --quiet pytest -q)
elif command -v pytest >/dev/null 2>&1; then
  runner=(pytest -q)
else
  # Тестового окружения ещё нет (до M1) — не блокируем.
  exit 0
fi

out="$("${runner[@]}" 2>&1)"; rc=$?

# rc=5 у pytest = «не собрано ни одного теста» — на пустом репозитории не провал.
if [ "$rc" -ne 0 ] && [ "$rc" -ne 5 ]; then
  {
    echo "БЛОК: тесты не проходят — коммит остановлен (ai_context/21, принцип №6)."
    echo "Команда: ${runner[*]}"
    echo "Почини красные тесты и повтори коммит. Последние строки прогона:"
    echo "$out" | tail -n 20
  } >&2
  exit 2
fi
exit 0
