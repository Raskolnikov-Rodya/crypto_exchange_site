# API Endpoints Reference (MVP)

Base URL (local):

- `http://localhost:8000/api/v1`

Useful non-versioned utility routes:

- `GET http://localhost:8000/`
- `GET http://localhost:8000/health`
- `GET http://localhost:8000/test-db`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

## Users (admin)

- `GET /users/`

## Wallet

- `GET /wallet/balances`
- `POST /wallet/deposit`
- `POST /wallet/withdraw/request`
- `GET /wallet/withdraw/requests`

## Trades

- `POST /trades/` (place order)
- `GET /trades/` (my order history)
- `GET /trades/orderbook/{symbol}`
- `POST /trades/match/{symbol}` (admin)

## Admin

- `GET /admin/transactions`
- `POST /admin/credit`
- `GET /admin/withdrawals`
- `POST /admin/withdrawals/{withdrawal_id}/approve`
- `POST /admin/withdrawals/{withdrawal_id}/reject`
- `POST /admin/withdrawals/{withdrawal_id}/complete`

## Prices

- `GET /prices/`

## Monitor (WebSocket)

- `WS /monitor/live_transactions`

## Blockchain (MVP stub)

- `GET /blockchain/status`

## Frontend API base URL

Frontend requests use:

- `VITE_API_URL` if set, otherwise
- default `http://localhost:8000/api/v1`

Defined in `frontend/src/services/api.js`.
