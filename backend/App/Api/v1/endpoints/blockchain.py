from fastapi import APIRouter, Depends, HTTPException
from app.services.blockchain import generate_wallet, get_wallet_balance, send_transaction, is_connected
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/status")
async def blockchain_status():
    """Check if blockchain is connected."""
    return {"connected": is_connected()}

@router.post("/generate_wallet")
async def create_user_wallet(user: User = Depends(get_current_user)):
    """Generate a new wallet for a user."""
    wallet = generate_wallet()
    return {"user_id": user.id, "wallet": wallet}

@router.get("/balance/{wallet_address}")
async def check_wallet_balance(wallet_address: str):
    """Check the balance of a given wallet address."""
    return get_wallet_balance(wallet_address)

@router.post("/send")
async def withdraw_crypto(to_address: str, amount: float, user: User = Depends(get_current_user)):
    """Send crypto to a user-specified address."""
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid withdrawal amount")

    # User must have a stored private key (This should be securely managed in production)
    if not hasattr(user, "private_key"):
        raise HTTPException(status_code=400, detail="No private key found for user")

    tx = send_transaction(user.private_key, to_address, amount)
    if "error" in tx:
        raise HTTPException(status_code=400, detail=tx["error"])

    return {"message": "Transaction sent", "tx_hash": tx["tx_hash"]}
