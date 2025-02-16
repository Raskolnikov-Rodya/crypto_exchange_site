from web3 import Web3
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.wallet import Wallet
from app.core.security import encrypt_private_key
from app.db.session import get_db
from sqlalchemy.future import select

# Connect to Ethereum Testnet (Sepolia via Infura)
INFURA_URL = os.getenv("INFURA_URL", "https://sepolia.infura.io/v3/YOUR_INFURA_PROJECT_ID")
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Check connection
def is_connected():
    return w3.isConnected()

# Generate a new Ethereum wallet for a user
def generate_wallet():
    """Generates a new Ethereum wallet (private key should be securely stored)."""
    account = w3.eth.account.create()
    return {
        "address": account.address,
        "private_key": account.key.hex()  # WARNING: Never expose private keys in production
    }

# Get ETH balance of a wallet
def get_wallet_balance(address: str):
    """Fetches ETH balance of a given wallet address."""
    if not Web3.isAddress(address):
        return {"error": "Invalid wallet address"}
    
    balance_wei = w3.eth.get_balance(address)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    return {"address": address, "balance": float(balance_eth)}

# Send ETH transaction (withdrawal)
def send_transaction(from_private_key: str, to_address: str, amount_eth: float):
    """Sends ETH from one address to another."""
    if not Web3.isAddress(to_address):
        return {"error": "Invalid recipient address"}

    # Get sender address from private key
    sender_account = w3.eth.account.from_key(from_private_key)
    
    # Build transaction
    tx = {
        'to': to_address,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': 21000,
        'gasPrice': w3.to_wei('50', 'gwei'),
        'nonce': w3.eth.get_transaction_count(sender_account.address)
    }

    # Sign transaction
    signed_tx = w3.eth.account.sign_transaction(tx, sender_account.key)
    
    # Send transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return {"tx_hash": tx_hash.hex()}
 
async def create_user_wallet(user_id: int, db: AsyncSession):
    """Creates and stores an encrypted wallet for a user."""
    account = w3.eth.account.create()
    
    encrypted_key = encrypt_private_key(account.key.hex())

    new_wallet = Wallet(
        user_id=user_id,
        address=account.address,
        encrypted_private_key=encrypted_key,
        currency="ETH"
    )
    
    db.add(new_wallet)
    await db.commit()
    return {"address": new_wallet.address}


async def withdraw_crypto(user_id: int, to_address: str, amount: float, db: AsyncSession):
    """Handles crypto withdrawals securely."""
    # Get user's wallet
    result = await db.execute(select(Wallet).where(Wallet.user_id == user_id, Wallet.currency == "ETH"))
    wallet = result.scalars().first()

    if not wallet:
        return {"error": "No wallet found"}

    # Validate recipient address
    if not Web3.isAddress(to_address):
        return {"error": "Invalid recipient address"}

    # Validate balance
    balance_data = get_wallet_balance(wallet.address)
    if balance_data["balance"] < amount:
        return {"error": "Insufficient balance"}

    # Decrypt private key for transaction
    private_key = decrypt_private_key(wallet.encrypted_private_key)
    
    # Send transaction
    return send_transaction(private_key, to_address, amount)