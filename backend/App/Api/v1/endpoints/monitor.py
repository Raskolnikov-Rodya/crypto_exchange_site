from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect
from app.core.logger import log_action
from loguru import logger

router = APIRouter()

# Store active WebSocket connections
active_connections = []

@router.websocket("/live_transactions")
async def monitor_transactions(websocket: WebSocket):
    """WebSocket to stream live transactions."""
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            message = await websocket.receive_text()
            if message == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def notify_clients(transaction_data):
    """Send transaction updates to all connected clients."""
    for connection in active_connections:
        try:
            await connection.send_json(transaction_data)
        except Exception as e:
            logger.error(f"Failed to send WebSocket message: {e}")