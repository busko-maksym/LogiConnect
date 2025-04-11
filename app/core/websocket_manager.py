from typing import Dict, List

from starlette.websockets import WebSocket


class ConnectionManager:

    def __init__(self) -> None:
        # active_connections will store a list of users for each chat_id
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, chat_id: str):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, websocket: WebSocket, chat_id: str):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)
            # If there are no more users in the chat, remove the chat_id
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def send_personal_message(self, message: str, websocket: WebSocket, chat_id: str):
        # Send a message to the specific websocket in the given chat_id
        if websocket in self.active_connections.get(chat_id, []):
            await websocket.send_text(message)

    async def broadcast(self, message: str, chat_id: str):
        # Broadcast message to all users in the specified chat_id
        for websocket in self.active_connections.get(chat_id, []):
            await websocket.send_text(message)


manager = ConnectionManager()
