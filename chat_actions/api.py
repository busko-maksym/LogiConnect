from fastapi import APIRouter, Depends, HTTPException
from user_actions.jwt_op import verify_token, decode_token
from chat_actions.appLogic import (create_chat, send_message,
                                   message_list, chats_list)
from chat_actions.models import Message
from fastapi import WebSocket, WebSocketDisconnect
import datetime
from chat_actions.appLogic import manager
from settings import customer_db, user_chat_db, messages_db
from bson import ObjectId, timestamp
import json
import re

router = APIRouter()


@router.post("/create")
async def cr_chat(second_user: str, decoded_token: dict = Depends(verify_token)):
    return await create_chat([decoded_token["user_id"], second_user])


@router.post("/{chat_id}/messages/send")
async def transfer_message(message: Message, chat_id: str, decoded_token: dict = Depends(verify_token)):
    return send_message(message, chat_id, decoded_token)


@router.post("/{chat_id}/messages")
async def get_messages(chat_id: str, decoded_token: dict = Depends(verify_token)):
    return message_list(chat_id, decoded_token)


@router.get("/")
async def get_chats(decoded_token: dict = Depends(verify_token)):
    return chats_list(decoded_token)


@router.websocket("/ws/{client_id}/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, client_id: str):
    await manager.connect(websocket, chat_id)
    decoded_token = decode_token(client_id)
    chat = user_chat_db.find_one({"_id": ObjectId(chat_id)})
    if chat is None or decoded_token["user_id"] not in chat["participants"]:
        manager.disconnect(websocket, chat_id)
    user = customer_db.find_one({"_id": ObjectId(decoded_token["user_id"])})

    try:
        while True:
            full_name = user["first_name"]+" "+user["last_name"]
            data = await websocket.receive_text()
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M")
            message = {"time": current_time, "name": full_name, "message": data}
            print(full_name)
            pattern_message = r'"message":"(.*?)"'
            match_message = re.search(pattern_message, data)
            if match_message:
                message_text = match_message.group(1)
            else:
                message_text = "Message not found"
            await manager.broadcast(json.dumps(message), chat_id)
            messages_db.insert_one({"sender_id": decoded_token["user_id"], "message": message_text,
                                    "chat_id": chat_id, "timestamp": current_time,
                                    "full_name": user["first_name"]+" "+user["last_name"]})

    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
