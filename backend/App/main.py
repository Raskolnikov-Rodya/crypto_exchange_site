from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

app = FastAPI(
    title="Crypto Exchange API",
    description="Simplified centralized crypto exchange (pet project)",
    version="0.1.0"
)

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