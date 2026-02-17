#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/6] pip metadata check"
python -m pip check || true

echo "[2/6] backend compile check"
python -m compileall backend/App backend/tests > /dev/null

echo "[3/6] backend model import check"
PYTHONPATH=backend python backend/test_import_models.py

echo "[4/6] backend app import + route count"
if python - <<'PY'
import importlib.util, sys
sys.exit(0 if importlib.util.find_spec("asyncpg") else 1)
PY
then
  python - <<'PY'
import os
os.chdir('backend')
from App.main import app
print('Route count:', len(app.routes))
PY
else
  echo "asyncpg not installed in current environment; skipping app import check"
fi

echo "[5/6] backend unit tests"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=backend pytest -q backend/tests/test_trading_engine.py

echo "[6/6] frontend dependency fetch check (informational)"
(
  cd frontend
  npm install --package-lock-only
) || echo "frontend dependency fetch failed (likely registry policy/network)"

echo "Dependency health check complete."
