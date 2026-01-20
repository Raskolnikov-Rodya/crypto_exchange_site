# backend/app/database.py

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()  # Loads from .env in backend/ (or project root if you placed it there)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in .env file!")

# Create the async engine
# echo=True will log SQL statements to console — great for learning/debugging
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,                   # ← Shows SQL in terminal when we run queries
    future=True                  # Enables SQLAlchemy 2.0 future-style API
)

async def test_db_connection() -> bool:
    """
    Simple async test: Connects to DB, runs SELECT 1, returns True if successful.
    """
    try:
        async with engine.connect() as conn:   # ← Opens an async connection
            # Run a trivial query
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()           # Gets the single value (should be 1)
            
            print("=== DB CONNECTION TEST SUCCESSFUL ===")
            print(f"Database responded with: {value}")
            print(f"Connected using URL: {DATABASE_URL}")
            print("=====================================")
            
            return True
    except Exception as e:
        print("=== DB CONNECTION TEST FAILED ===")
        print(f"Error: {str(e)}")
        return False


# Quick way to run the test from command line (for now)
if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_db_connection())
    if not success:
        exit(1)