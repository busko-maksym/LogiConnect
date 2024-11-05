from fastapi import APIRouter, Depends, HTTPException
from user_actions.jwt_op import verify_token
from chat_actions.appLogic import create_chat, send_message, message_list
from chat_actions.models import Message

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
