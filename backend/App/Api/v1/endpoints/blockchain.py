from fastapi import APIRouter

router = APIRouter()


@router.get("/status")
async def blockchain_status():
    return {
        "connected": False,
        "message": "Blockchain broadcasting is not enabled in MVP mode. Use internal ledger + manual admin flow.",
    }
