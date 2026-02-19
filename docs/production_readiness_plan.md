# Production Readiness Plan (1–2 Weeks)

This plan is designed to improve reliability without introducing risky refactors.

## Goal
Ship a predictable, observable, and secure MVP to production with low regression risk.

## Week 1 — Stabilize and Prove Core Flows

### 1) CI as a gate (must pass)
- Run backend compile + tests (unit + API flow integration).
- Run frontend production build.
- Block merges on CI failures.

Reference workflow: `.github/workflows/ci.yml`.

### 2) Deterministic operator onboarding
- Use `scripts/bootstrap_admin.py` to create/promote admin accounts in staging/prod.
- Document exact command in `docs/local_setup_and_run.md`.

### 3) Preflight before deploy
- Use `scripts/prod_preflight.sh` to check:
  - env sanity (`DATABASE_URL`, secure JWT in production)
  - compile checks
  - backend tests
  - conditional integration tests
  - frontend build

### 4) Release checklist for every deployment
- DB migration run and verified.
- `/health` and `/test-db` verified after deploy.
- Manual smoke for: register/login/profile/wallet/trade/admin queue.

## Week 2 — Operability and Risk Reduction

### 5) Observability baseline
- Add request-id-aware structured logging and central log collection.
- Create alerts for:
  - auth failures spike
  - 5xx rate spike
  - DB connectivity failures

### 6) Security and config hardening
- Store secrets in deployment secret manager (not `.env` in servers).
- Rotate JWT secret before production launch if default/dev value was ever used.
- Tighten CORS to actual deployed frontend origins only.

### 7) Runbooks and rollback readiness
- Create runbook for rollback and migration rollback strategy.
- Keep one-click re-deploy to last known good commit.

## Go / No-Go Criteria

### Go if all are true
- CI green on target commit.
- Preflight script green in deploy environment.
- API flow tests pass in CI.
- Manual smoke in staging completed successfully.

### No-Go if any are true
- API flow tests skipped/failed in target environment.
- DB connectivity instability remains unresolved.
- Admin bootstrap process is unclear or untested.
- No rollback path is documented and tested.
