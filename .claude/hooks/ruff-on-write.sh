#!/usr/bin/env bash
# PostToolUse-хук: после того как Claude отредактировал .py-файл под app/,
# прогнать по нему `ruff check --fix` + `ruff format`.
# Это «автоповедение реализуется хуком, не памятью» из ai_context/14 §11.4
# и гейт стиля/типов из ai_context/M1 «Общие требования».
#
# Вход: JSON события хука на stdin (поле tool_input.file_path).
# jq в системе может не быть → парсим stdin через python3.
set -euo pipefail

payload="$(cat)"
f="$(printf '%s' "$payload" | python3 -c 'import sys,json
try:
    d = json.load(sys.stdin)
except Exception:
    print(""); sys.exit(0)
print(d.get("tool_input", {}).get("file_path") or d.get("tool_response", {}).get("filePath") or "")' 2>/dev/null || true)"

[ -z "$f" ] && exit 0

# только Python-файлы внутри app/
case "$f" in
  *"/app/"*.py|"app/"*.py) ;;
  *) exit 0 ;;
esac

[ -f "$f" ] || exit 0

if ! command -v ruff >/dev/null 2>&1; then
  printf '{"systemMessage":"ruff не установлен — авто-формат пропущен (см. ai_context/06-stek-po-modulyam.md)"}\n'
  exit 0
fi

ruff check --fix "$f" >/dev/null 2>&1 || true
ruff format "$f" >/dev/null 2>&1 || true
exit 0
