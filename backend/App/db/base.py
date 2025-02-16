from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
 

 # Import models to ensure they are registered
from app.models.user import User
from app.models.trade import Trade
from app.models.wallet import Wallet

# Function to create tables
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
