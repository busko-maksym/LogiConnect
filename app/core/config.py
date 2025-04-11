import fastapi
from aiogram import Dispatcher

from app.core.security import client

app = fastapi.FastAPI()
dp = Dispatcher()
user_db = client["Users_db"]
chat_db = client["Chat"]
vacancies = client["Vacancies"]
messages_db = chat_db["messages"]
user_chat_db = chat_db["chats"]
vacancies_db = vacancies["vacancies"]
history_db = vacancies["history"]
filters_db = user_db["filters"]
customer_db = user_db["customer"]
cars_db = user_db["cars"]
beta_users = user_db["beta_users"]
