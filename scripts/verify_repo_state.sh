#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/6] Checking unresolved merge files..."
if git ls-files -u | grep -q .; then
  echo "Unmerged files detected"
  exit 1
fi

echo "[2/6] Checking conflict markers in key backend/docs files..."
rg -n "^<<<<<<<|^=======|^>>>>>>>" backend/App docs && {
  echo "Conflict markers found"
  exit 1
} || true

echo "[3/6] Checking legacy import paths (app.*)"
if rg -n "from app\.|import app\.|app\.db|app\.api" backend/App backend/migrations backend/test_import_models.py; then
  echo "Legacy import paths detected"
  exit 1
fi

echo "[4/6] Compile check"
python -m compileall backend/App backend/tests docs > /dev/null

echo "[5/6] Unit tests"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=backend pytest -q backend/tests/test_trading_engine.py backend/tests/test_security.py

echo "[6/6] API integration smoke tests"
if python - <<'PY'
import importlib.util, sys
sys.exit(0 if importlib.util.find_spec("aiosqlite") else 1)
PY
then
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=backend pytest -q backend/tests/test_api_flows.py
else
  echo "aiosqlite not installed; skipping API integration smoke tests"
fi

echo "Repository verification passed."
