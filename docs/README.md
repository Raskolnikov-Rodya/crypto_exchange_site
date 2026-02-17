 # Crypto Exchange Site

A simplified, centralized cryptocurrency exchange platform inspired by KuCoin, built as a personal pet project.

**Core Philosophy**:
- Real cryptocurrencies: USDT (base), BTC, ETH, LTC, BCH.
- Centralized: All deposits/withdrawals go through single control wallets (one per coin) that you manage.
- Manual admin review: Deposits credited manually after external verification (e.g., email/screenshot); withdrawals require admin approval.
- Internal trading only: Full limit order book with real market prices, but trades update internal DB balances (no blockchain execution).
- Production-ready mindset: Security basics, logging, Docker support from early stages.

**Supported Pairs** (USDT-based only):
- BTC/USDT
- ETH/USDT
- LTC/USDT
- BCH/USDT

**Fees**:
- Trading: 0.1% per trade (deducted from received amount)
- Withdrawal: 0.1% + network fees (platform takes 0.1%)
- Deposits: Free (only external network fees)

**Key Constraints**:
- Minimum withdrawal: $50 (equivalent in coin)
- No KYC, no per-user deposit addresses
- Withdrawals: Pending message to user → "In progress, ~30 minutes" while in queue

**Tech Stack**:
- Backend: FastAPI (Python), SQLAlchemy + PostgreSQL
- Frontend: React.js + CoreUI free admin template
- Blockchain utils: web3.py (ETH/USDT), python-bitcoinlib (BTC/LTC/BCH)
- Prices: CoinGecko API (periodic + WebSockets)
- Auth: fastapi-users
- Tasks: Celery (optional for price polling)

**Status**: Planning → Documentation → Setup

See /docs/ for detailed specs.

## Additional Planning
- Codebase audit and execution roadmap: `docs/codebase_audit.md`
- Progress report: `docs/progress_report.md`
- Phase 4 runbook/checklist: `docs/phase4_runbook.md`
- Local setup and run guide: `docs/local_setup_and_run.md`
- Optional backend dependencies: `backend/requirements-optional.txt`
