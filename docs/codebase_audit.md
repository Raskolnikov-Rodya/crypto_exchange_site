# Codebase Audit & Forward Plan

## Executive Summary

The project has a solid product direction in documentation, but the implementation is currently at an early scaffold stage. The highest risk is **architectural inconsistency** (mixed module paths, duplicate API structures, many empty files), which will block reliable development unless normalized first.

This is still very feasible to bring live, but it needs a strict sequence:
1. Stabilize backend structure and imports.
2. Complete minimal backend vertical slice (auth + balances + deposits/withdrawals).
3. Rebuild frontend around a small working API contract.
4. Add trading engine and operations workflows.

## What Is Working Well

- Product scope and operating constraints are clearly documented (MVP, manual ops flow, fee model, supported pairs).
- Database and migration tooling are already present (SQLAlchemy + Alembic).
- Docker Compose exists to support local multi-service development.

## Key Issues Found

### 1) Conflicting backend package layout

There are multiple conventions in use at once:
- `backend/App/...` filesystem layout.
- Imports using `app.*` (lowercase) that do not match on case-sensitive systems.
- Endpoint files referencing modules that do not exist (`app.db.session`, `app.models.trade`, `app.db.base`).

This will cause immediate runtime failures when routing imports are executed.

### 2) Duplicate and split API structures

Two API trees exist:
- `App/routers/*` (mostly empty files).
- `App/Api/v1/endpoints/*` (contains implementation attempts).

Having both slows progress and creates ambiguity on where to add features.

### 3) Several files are placeholders/empty

Many frontend and backend files are empty or near-empty. This is normal early on, but currently prevents an end-to-end runnable flow.

### 4) Model inconsistencies

- `wallet.py` imports `app.db.base` while other models use local `.base`.
- `transaction.py` references `datetime`/`ZoneInfo` without importing them.
- Relationship patterns are partially duplicated and inconsistent.

### 5) Security and operations not yet production-safe

Given the business model (custodial funds, admin queues), current code is not yet safe for live use. A private alpha with testnet/sandbox assets is feasible after foundational cleanup.

## Feasibility Assessment

- **Very feasible** as an MVP if you target a centralized internal ledger first.
- **Not yet feasible** for public launch until architecture cleanup and minimal security controls are complete.

## Recommended Development Roadmap

## Phase 0 (1-2 days): Normalize architecture

- Choose one canonical backend package path (`App` or `app`) and apply consistently.
- Keep one API structure (`Api/v1/endpoints` OR `routers`) and delete/archive the other.
- Ensure `main.py` mounts every router and app starts cleanly.
- Remove duplicate imports and dead placeholders.

**Done when:** `uvicorn` boots, `/health` works, and import errors are gone.

## Phase 1 (3-5 days): Core account ledger

- Implement users, balances, and transaction ledger with clean schemas.
- Add register/login/JWT with role checks.
- Add admin-only endpoint to manually credit deposits.
- Add withdrawal request object and state transitions (`pending -> approved/rejected -> completed`).

**Done when:** A user can register, view balances, request withdrawal, and admin can process queue.

## Phase 2 (3-6 days): Frontend vertical slice

- Rebuild frontend around 4-6 stable API endpoints.
- Implement auth screens + dashboard balance view + withdrawal form + admin queue page.
- Keep UI minimal; avoid complex charting until flows are stable.

**Done when:** Basic user and admin workflows are usable in browser.

## Phase 3 (5-8 days): Trading MVP

- Add order + trade models and deterministic matching logic (price-time priority).
- Add fee handling in one place (service-level function).
- Expose order book and trade history endpoints.
- Add tests for matching and balance settlement.

**Done when:** Internal matching executes and updates balances correctly.

## Phase 4 (2-4 days): Hardening before any public beta

- Add env validation and secrets handling.
- Add request validation and rate limiting on auth-sensitive endpoints.
- Add audit logging for admin financial actions.
- Add backup/recovery checklist and runbook.

## Immediate Next Tasks (Suggested This Week)

1. Pick canonical package naming and refactor imports.
2. Wire a single router tree into `main.py`.
3. Fix model import/runtime errors and run migrations from clean DB.
4. Build one complete user story: register -> login -> get balance -> request withdrawal -> admin approve.
5. Add smoke tests for auth, balances, withdrawals.

## Suggested Scope Guardrails

To avoid stalling:
- Defer real blockchain send logic and WebSockets until internal ledger correctness is verified.
- Defer advanced UI polish and multi-chain abstractions.
- Keep all monetary values as Decimal/Numeric (avoid float for balances).

## Final Recommendation

You are not “doing it wrong”; you are at a common prototype stage where ideas are ahead of code consistency. The project is worth continuing. Focus on architecture cleanup first, then complete one vertical slice end-to-end before expanding features.
