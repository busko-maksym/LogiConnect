import app.services
from app.core.config import beta_users
from app.utils import send_email


async def messaging(message):
    users = list(beta_users.find())  # Convert cursor to list
    for user in users:
        try:
            await app.services.chat.chat.send_message(user["telegram"], message)
        except Exception:
            send_email(message, user["email"])

    return {"msg": "Your message has been sent"}
