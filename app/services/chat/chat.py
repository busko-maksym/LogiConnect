from datetime import datetime
from typing import List

from bson import ObjectId

from app.core.config import user_chat_db, customer_db, messages_db
from app.core.security import site_directory
from app.models.chat import Chat


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
    users = user_chat_db.find({"participants": {"$in": [token["user_id"]]}})
    users_list = []

    for user in users:
        user['_id'] = str(user['_id'])
        other_participants = [p for p in user['participants'] if p != token["user_id"]]

        other_user_id = other_participants[0]
        second_user = customer_db.find_one({"_id": ObjectId(other_user_id)})

        if second_user:
            user['name'] = str(second_user['first_name']+" "+second_user['last_name'])
        else:
            user['name'] = "Deleted account"
        users_list.append(user)

    return {"msg": users_list}
