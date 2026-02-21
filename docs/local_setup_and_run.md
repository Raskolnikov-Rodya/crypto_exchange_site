# Local Setup & Run Guide

If you see this error:

```text
ModuleNotFoundError: No module named 'fastapi'
```

it means Python dependencies are not installed in your active environment yet.

## Important clarification

- `fastapi`, `web3.py`, and similar libraries are **Python packages**, not project folders in this repo.
- `CoreUI` is a frontend dependency/template ecosystem, not expected as a Python folder.
- Empty local folders with those names are not required for this project to run.

## Backend (Windows PowerShell)

From repo root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd backend
alembic upgrade head
python run_api.py
```

Backend should start at `http://localhost:8000`.

## Backend (Linux/macOS)

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd backend
alembic upgrade head
python run_api.py
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend should start on Vite default port (usually `http://localhost:5173`).


## Frontend opens to a blank white page

If Vite starts but the page is blank, check these in order:

1. Open browser DevTools Console for runtime errors (missing module, network, CORS).
2. Confirm frontend deps are installed in `frontend/`:
   - `npm install`
3. Confirm backend is running:
   - `cd backend && python run_api.py`
4. Verify backend is reachable:
   - `http://localhost:8000/health`
   - `http://localhost:8000/docs`
5. Ensure frontend points to the correct API base URL:
   - default is `http://localhost:8000/api/v1`
   - override with `.env` in `frontend/`:

```bash
VITE_API_URL=http://localhost:8000/api/v1
```

6. Hard-refresh the browser (Ctrl+F5) and clear stale localStorage token if needed.

### Do I need API keys to see the app?

- For core MVP pages (home, login, signup, dashboard shell), **no API keys are required**.
- The `prices` API calls CoinGecko anonymously in current MVP mode; no key is required in this repo setup.
- Blockchain broadcasting is intentionally disabled in MVP (`/api/v1/blockchain/status` returns a stub status).

### Recommended URLs to test

- Frontend app: `http://localhost:5173/`
- Backend health: `http://localhost:8000/health`
- Backend Swagger docs: `http://localhost:8000/docs`
- API reference in repo: `docs/api_endpoints_reference.md`


## Database prerequisite (important)

Most API routes (login/register, wallet, trades, admin) need a running PostgreSQL instance matching `DATABASE_URL`.
If Postgres is not running, those routes will fail (typically 500/503).

Quick checks:

- `GET http://localhost:8000/health` (app process is up)
- `GET http://localhost:8000/test-db` (database connectivity)

If `/test-db` reports database unavailable, start PostgreSQL and verify `.env` `DATABASE_URL`.



## Bootstrap an admin account

The dashboard only shows the admin panel for users with role `admin`.
After running migrations, bootstrap an admin user:

```bash
PYTHONPATH=backend python scripts/bootstrap_admin.py \
  --email admin@example.com \
  --password AdminPass123 \
  --username admin
```

Then sign in with that account on `/login` and open `/dashboard`.

## Docker: promote a user to admin

After your containers are up, you can promote/create an admin from inside the backend container:

```bash
docker compose exec backend \
  env PYTHONPATH=/app/backend \
  python /app/scripts/bootstrap_admin.py \
  --email admin@example.com \
  --password AdminPass123 \
  --username admin
```

Then sign in with that account and open `/dashboard` to access admin controls.

## Frontend pages and backend endpoint alignment

Implemented pages and route wiring:

- `/login` -> `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- `/signup` -> `POST /api/v1/auth/register`
- `/dashboard` (user) -> wallet flows:
  - `GET /api/v1/wallet/balances`
  - `POST /api/v1/wallet/deposit`
  - `POST /api/v1/wallet/withdraw/request`
  - `GET /api/v1/wallet/withdraw/requests`
- `/dashboard` (admin role) -> admin flows:
  - `GET /api/v1/users/`
  - `GET /api/v1/admin/transactions`
  - `POST /api/v1/admin/credit`
  - `GET /api/v1/admin/withdrawals`
  - `POST /api/v1/admin/withdrawals/{id}/approve|reject|complete`
- `/trade` -> trading flows:
  - `POST /api/v1/trades/`
  - `GET /api/v1/trades/`
  - `GET /api/v1/trades/orderbook/{symbol}`

If a page stays blank, clear localStorage key `ce_token` and hard refresh.


## Production preflight command

Before a release candidate deployment, run:

```bash
bash scripts/prod_preflight.sh
```

This runs compile checks, backend tests, conditional API flow smoke tests, frontend build, and repo-state verification in one command.

## What to test first

1. Backend health: `GET http://localhost:8000/health`
2. Auth register/login flow (`/api/v1/auth/register`, `/api/v1/auth/login`)
3. Dashboard flow in frontend (login, balances, withdrawal request)
4. Admin queue actions for withdrawals

## Common mistakes

- Running `python backend/App/main.py` directly (not recommended).
- Using global Python without activating virtualenv.
- Installing frontend dependencies but not backend dependencies (or vice versa).



## Troubleshooting: `column users.username does not exist`

If login/register returns 500 and backend logs show:

```text
column users.username does not exist
```

then your database is behind the current schema version. Run migrations from `backend/`:

```bash
alembic upgrade head
```

Then restart the API process.

## Troubleshooting: `pg_config executable not found`

If `pip install -r backend/requirements.txt` fails with:

```text
Error: pg_config executable not found
```

it means your environment is trying to compile an old psycopg2 dependency from source.
This project now uses `psycopg[binary]` in requirements to avoid that build step.

Try:

```powershell
pip install --upgrade pip setuptools wheel
pip install -r backend/requirements.txt
```

Also prefer Python 3.10–3.12 for the smoothest package wheel compatibility.


## Troubleshooting: `pydantic-core` metadata generation / Rust error

If installation fails with messages about `pydantic-core` and Rust/Cargo while using Python 3.14,
it usually means pip could not find a compatible prebuilt wheel for your pinned package version.

This repo now pins newer FastAPI/Pydantic versions to improve wheel availability on modern Python.

Try this sequence:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip uninstall -y pydantic pydantic-core pydantic-settings
pip install -r backend/requirements.txt
```

If it still tries to compile Rust extensions, use Python 3.12 in your virtualenv for now:

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```


## Optional packages (only if you need them now)

Some optional integrations (not required for current MVP runtime) may require native build tools on Windows.
Install them only when needed:

```powershell
pip install -r backend/requirements-optional.txt
```

Examples:
- `web3` (blockchain integrations)
- `ccxt` (exchange integrations)
- `celery` + `redis` (background jobs)


## Troubleshooting: `lru-dict` wheel build / MSVC error

If you see:

```text
Microsoft Visual C++ 14.0 or greater is required
```

it is usually from optional dependencies (commonly `web3` transitive packages) requiring native wheels/build tools on your platform.

Recommended path:
1. Install only core requirements first (`backend/requirements.txt`).
2. Run backend and verify MVP flows.
3. Install optional requirements later only when you need those features.

If you must install optional packages immediately, install Microsoft C++ Build Tools first.


## Why `GET /api/v1` returns 404

`/api/v1` is a router prefix, not a standalone endpoint.
Use concrete routes such as `/api/v1/auth/register`, `/api/v1/auth/login`, `/api/v1/wallet/balances`, etc.
