from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class Message(BaseModel):
    sender_id: str = None
    chat_id: str = None
    message: str
    timestamp: datetime = datetime.now()


class Chat(BaseModel):
    participants: List[str]
    last_message: str = None
    updated_at: datetime = datetime.now()
