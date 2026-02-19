import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("crypto_exchange.error_handler")


async def http_error_handler(request: Request, exc: HTTPException):
    """Handles all HTTP exceptions."""
    logger.error("Error: %s, Status Code: %s, Path: %s", exc.detail, exc.status_code, request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handles unexpected errors."""
    logger.exception("Unexpected server error on path: %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "An unexpected error occurred. Please try again later."},
    )
