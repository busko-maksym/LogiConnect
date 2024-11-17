from chat_actions.models import Chat
from settings import user_chat_db, customer_db, messages_db, site_directory
from typing import List
from bson import ObjectId
from datetime import datetime
from typing import Dict, List
from fastapi import WebSocket


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


async def create_chat(participants: List[str]):
    chat = user_chat_db.find_one({"participants": {"$all": participants}})

    if chat:
        return str(chat['_id'])

    second_user = customer_db.find_one({"_id": ObjectId(participants[1])})

    if second_user is None:
        return {"msg": "User not found"}

    new_chat = Chat(participants=participants)
    result = user_chat_db.insert_one(new_chat.__dict__)

    return {"chat_id": str(result.inserted_id),
            "link": f"{site_directory}/chat/{str(result.inserted_id)}"}


def send_message(message, chat_id, user):
    message_data = dict(message)
    message_data['timestamp'] = datetime.now()
    message_data['chat_id'] = chat_id
    message_data['sender_id'] = user["user_id"]
    result = messages_db.insert_one(message_data)

    messages_db.chats.update_one(
        {"_id": ObjectId(message_data["chat_id"])},
        {
            "$set": {
                "last_message": str(result.inserted_id),
                "updated_at": datetime.now()
            }
        }
    )

    return {"message_id": str(result.inserted_id)}


def message_list(chat_id, user):

    chat = user_chat_db.find_one({"_id": ObjectId(chat_id)})
    messages = messages_db.find({'chat_id': chat_id})

    x = []
    for message in messages:
        message['_id'] = str(message['_id'])
        x.append(message)

    if user["user_id"] in chat["participants"]:
        return x
    else:
        return {"msg": "User not found"}


def chats_list(token):
    user_chat_db.find({"locations": {"$in": [token["user_id"]]}})


