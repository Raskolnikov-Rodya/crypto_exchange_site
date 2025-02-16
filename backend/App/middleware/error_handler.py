from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger

async def http_error_handler(request: Request, exc: HTTPException):
    """Handles all HTTP exceptions"""
    logger.error(f"Error: {exc.detail}, Status Code: {exc.status_code}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

async def generic_exception_handler(request: Request, exc: Exception):
    """Handles unexpected errors"""
    logger.exception("Unexpected server error")
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later."}
    )
