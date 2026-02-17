from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect

router = APIRouter()
active_connections: list[WebSocket] = []


@router.websocket("/live_transactions")
async def monitor_transactions(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            if message == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)


async def notify_clients(event: dict):
    disconnected: list[WebSocket] = []
    for connection in active_connections:
        try:
            await connection.send_json(event)
        except Exception:
            disconnected.append(connection)
    for ws in disconnected:
        if ws in active_connections:
            active_connections.remove(ws)
