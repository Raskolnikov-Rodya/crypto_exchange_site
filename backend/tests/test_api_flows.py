import os
from pathlib import Path
import importlib.util

import pytest

if importlib.util.find_spec("aiosqlite") is None:
    pytest.skip("aiosqlite is required for API integration flow tests", allow_module_level=True)

from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Ensure App.database can import during test startup.
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./test_bootstrap.db")

from App.database import get_db
from App.main import app
from App.models import Base
from App.models.user import Role, User


@pytest.fixture()
def client() -> TestClient:
    test_db_path = Path("backend/tests/test_api_flows.db")
    if test_db_path.exists():
        test_db_path.unlink()

    engine = create_async_engine(f"sqlite+aiosqlite:///{test_db_path}", future=True)
    session_local = async_sessionmaker(engine, expire_on_commit=False)

    async def override_get_db():
        async with session_local() as session:
            yield session

    async def prepare_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()

    import asyncio

    asyncio.run(prepare_db())
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    asyncio.run(teardown_db())
    if test_db_path.exists():
        test_db_path.unlink()


def _register(client: TestClient, email: str, password: str, username: str | None = None):
    payload = {"email": email, "password": password}
    if username:
        payload["username"] = username
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()


def _login_token(client: TestClient, email: str, password: str) -> str:
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _promote_user_to_admin(email: str) -> None:
    async def run_update():
        db = app.dependency_overrides[get_db]
        async for session in db():
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalar_one()
            user.role = Role.ADMIN
            await session.commit()

    import asyncio

    asyncio.run(run_update())


def test_auth_register_login_and_profile_roundtrip(client: TestClient):
    _register(client, "alice@example.com", "SecurePass1", "alice")
    token = _login_token(client, "alice@example.com", "SecurePass1")

    me = client.get("/api/v1/auth/me", headers=_auth_headers(token))
    assert me.status_code == 200, me.text
    assert me.json()["email"] == "alice@example.com"

    update = client.patch(
        "/api/v1/users/me",
        json={"phone": "+1234567"},
        headers=_auth_headers(token),
    )
    assert update.status_code == 200, update.text
    assert update.json()["phone"] == "+1234567"

    change_password = client.post(
        "/api/v1/users/me/password",
        json={"current_password": "SecurePass1", "new_password": "EvenBetter2"},
        headers=_auth_headers(token),
    )
    assert change_password.status_code == 200, change_password.text

    relogin = _login_token(client, "alice@example.com", "EvenBetter2")
    assert relogin


def test_wallet_trade_and_admin_withdrawal_flow(client: TestClient):
    _register(client, "admin@example.com", "AdminPass1", "admin")
    _register(client, "buyer@example.com", "BuyerPass1", "buyer")
    _register(client, "seller@example.com", "SellerPass1", "seller")
    _promote_user_to_admin("admin@example.com")

    admin_token = _login_token(client, "admin@example.com", "AdminPass1")
    buyer_token = _login_token(client, "buyer@example.com", "BuyerPass1")
    seller_token = _login_token(client, "seller@example.com", "SellerPass1")

    dep_quote = client.post(
        "/api/v1/wallet/deposit",
        json={"coin": "USDT", "amount": "1000"},
        headers=_auth_headers(buyer_token),
    )
    assert dep_quote.status_code == 200, dep_quote.text

    dep_base = client.post(
        "/api/v1/wallet/deposit",
        json={"coin": "BTC", "amount": "1"},
        headers=_auth_headers(seller_token),
    )
    assert dep_base.status_code == 200, dep_base.text

    buy_order = client.post(
        "/api/v1/trades/",
        json={"side": "buy", "symbol": "BTC/USDT", "price": "100", "amount": "0.5"},
        headers=_auth_headers(buyer_token),
    )
    assert buy_order.status_code == 200, buy_order.text

    sell_order = client.post(
        "/api/v1/trades/",
        json={"side": "sell", "symbol": "BTCUSDT", "price": "99", "amount": "0.5"},
        headers=_auth_headers(seller_token),
    )
    assert sell_order.status_code == 200, sell_order.text

    match = client.post("/api/v1/trades/match/BTCUSDT", headers=_auth_headers(admin_token))
    assert match.status_code == 200, match.text
    assert match.json()["matches"] >= 1

    withdraw_req = client.post(
        "/api/v1/wallet/withdraw/request",
        json={"coin": "BTC", "amount": "0.1", "destination_address": "bc1qexample"},
        headers=_auth_headers(buyer_token),
    )
    assert withdraw_req.status_code == 200, withdraw_req.text
    withdrawal_id = withdraw_req.json()["id"]

    approve = client.post(
        f"/api/v1/admin/withdrawals/{withdrawal_id}/approve",
        json={"note": "looks good"},
        headers=_auth_headers(admin_token),
    )
    assert approve.status_code == 200, approve.text
    assert approve.json()["status"] == "approved"

    complete = client.post(
        f"/api/v1/admin/withdrawals/{withdrawal_id}/complete",
        json={"tx_hash": "0xabc"},
        headers=_auth_headers(admin_token),
    )
    assert complete.status_code == 200, complete.text
    assert complete.json()["status"] == "completed"

    admin_users = client.get("/api/v1/users/", headers=_auth_headers(admin_token))
    assert admin_users.status_code == 200
    assert len(admin_users.json()) >= 3
