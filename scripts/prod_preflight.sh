#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/6] Required environment sanity"
PYTHONPATH=backend python - <<'PY'
from App.core.config import settings

problems = []
if settings.ENV.lower() == "production":
    if settings.JWT_SECRET == "your-secret-key" or len(settings.JWT_SECRET) < 32:
        problems.append("JWT_SECRET is weak for production")
if not settings.DATABASE_URL:
    problems.append("DATABASE_URL missing")
if problems:
    raise SystemExit("; ".join(problems))
print("Environment settings look valid")
PY

echo "[2/6] Python compile checks"
python -m compileall backend/App backend/tests docs > /dev/null

echo "[3/6] Unit tests"
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=backend pytest -q backend/tests/test_trading_engine.py backend/tests/test_security.py

echo "[4/6] API integration smoke tests (conditional)"
if python - <<'PY'
import importlib.util, sys
sys.exit(0 if importlib.util.find_spec("aiosqlite") else 1)
PY
then
  PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=backend pytest -q backend/tests/test_api_flows.py
else
  echo "aiosqlite not installed; skipping API flow tests"
fi

echo "[5/6] Frontend build"
(
  cd frontend
  npm run build > /dev/null
)

echo "[6/6] Repo verification"
bash scripts/verify_repo_state.sh > /dev/null

echo "Preflight checks passed."
