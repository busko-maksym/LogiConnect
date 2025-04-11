from app.core.config import dp, customer_db, beta_users
from app.core.security import TOKEN, redis_conn, site_directory
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import types, Bot
from aiogram.filters import CommandStart
import json
from bson import ObjectId

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    if len(message.text.split()) == 1:
        await message.reply(f"Welcome! this is notifications bot and you have"
                            f" to go to this bot through our website: {site_directory}")
        return

    args = message.text.split()[1]

    if args.split("-")[0] == "beta":
        user = beta_users.find_one({"_id": ObjectId(args.split("-")[1])})
        beta_users.update_one(user, {"$set": {"telegram": message.from_user.id,
                                              "telegram_username": message.from_user.username}})
        await message.reply("you connected telegram, thanks!")
        return
    elif args.split("-")[0] == "connect":
        pass
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
    print(message.from_user.id)
    await message.reply("this bot can only send you notifications, nothing else")
