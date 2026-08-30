#!/usr/bin/env bash
# Generate both project variants from the template and assert they lint clean
# (using each project's OWN ruff config) and that the non-torch one runs.
# Note: copier reads the template's committed git state — commit before testing.
set -euo pipefail

OS="$(cd "$(dirname "$0")" && pwd)"
export PATH="$HOME/.local/bin:/home/linuxbrew/.linuxbrew/bin:$PATH"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

gen() {  # $1 = name, $2 = use_torch
  copier copy --trust --defaults \
    --data project_name="$1" --data project_slug="$1" \
    --data question="template regression test" --data use_torch="$2" \
    --data sconixlib_path="$OS/sconixlib" --data created_at="2026-01-01" \
    "$OS/template" "$WORK/$1" >/dev/null
}

echo ":: non-torch variant"
gen nontorch false
( cd "$WORK/nontorch"
  TMPDIR=/tmp uv sync --all-groups >/dev/null 2>&1
  uv run ruff check .
  uv run ruff format --check . >/dev/null
  TMPDIR=/tmp uv run python experiments/exp001_smoke/run.py >/dev/null
  TMPDIR=/tmp uv run pytest -q >/dev/null
)
echo ":: non-torch OK (lint + run + test)"

echo ":: torch variant (lint only; torch wheel served from uv cache)"
gen torchproj true
( cd "$WORK/torchproj"
  TMPDIR=/tmp uv sync --all-groups >/dev/null 2>&1
  uv run ruff check .
  uv run ruff format --check . >/dev/null
)
echo ":: torch OK (lint)"

echo "ALL TEMPLATE CHECKS PASSED"
