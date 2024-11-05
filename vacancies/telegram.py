from settings import dp, TOKEN
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types, Bot
from aiogram.filters import CommandStart
from settings import site_directory, redis_conn
from settings import customer_db
import json

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    if len(message.text.split()) == 1:
        await message.reply(f"Welcome! No code was provided, you need"
                            f" to go to this bot through our website: {site_directory}")
        return
    print((message.text.split()))
    args = message.text.split()[1]
    connection_obj = redis_conn.get(args)
    if connection_obj:
        json_mail = json.loads(connection_obj)
        user = customer_db.find_one({"email": json_mail["email"]})
        customer_db.update_one({"email": json_mail["email"]},
                               {"$set": {"telegram": message.from_user.id}})
        redis_conn.delete(args)
        await message.reply(f"Your account notifications successfully connected, if "
                            f"{user["first_name"].capitalize()} {user['last_name'].capitalize()}"
                            f" isn`t you, you can remake connect")
    else:
        await message.reply(f"Welcome! No code was provided, you need"
                            f" to go to this bot through our website{site_directory}")


@dp.message()
async def handle_message(message: types.Message):
    print(message)
