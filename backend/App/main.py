# backend/app/main.py

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, engine  # ← Import from same folder
from .database import get_db, engine, Base
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import os

load_dotenv()

app = FastAPI(
    title="Crypto Exchange API",
    description="Simplified centralized crypto exchange (pet project)",
    version="0.1.0"
)

#Alembic migrations will handle table creation
# Startup event: Create tables if they don't exist
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # --- Startup Logic ---
#     async with engine.begin() as conn:
#         # metadata.create_all is a sync function, so we use run_sync
#         await conn.run_sync(Base.metadata.create_all)
#     print("=== Tables created successfully (or already exist) ===")

#     yield

# app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World! Welcome to the Crypto Exchange API"}


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": os.getenv("ENV", "development"),
        "database_url": "configured" if os.getenv("DATABASE_URL") else "missing"
    }


@app.get("/test-db")
async def test_db_connection(db: AsyncSession = Depends(get_db)):
    """
    Endpoint that actually queries the DB via dependency.
    """
    try:
        # Simple test query
        result = await db.execute(text("SELECT 1"))
        value = result.scalar()
        
        return {
            "status": "success",
            "message": "Database connection works!",
            "db_response": value,
            "database_url": os.getenv("DATABASE_URL")
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }