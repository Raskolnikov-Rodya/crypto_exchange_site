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
python run_api.py
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend should start on Vite default port (usually `http://localhost:5173`).

## What to test first

1. Backend health: `GET http://localhost:8000/health`
2. Auth register/login flow (`/api/v1/auth/register`, `/api/v1/auth/login`)
3. Dashboard flow in frontend (login, balances, withdrawal request)
4. Admin queue actions for withdrawals

## Common mistakes

- Running `python backend/App/main.py` directly (not recommended).
- Using global Python without activating virtualenv.
- Installing frontend dependencies but not backend dependencies (or vice versa).


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
