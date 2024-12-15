import pymongo
import fastapi
import redis
from aiogram import Bot, Dispatcher
from os import getenv

app = fastapi.FastAPI()

client = pymongo.MongoClient("mongodb+srv://yanamefi:gKAE9hAGHqkVYoCm@cluster0.o22hb.mongodb.net"
                             "/?retryWrites=true&w=majority&appName=Cluster0")

TOKEN = "7835528925:AAEEayAqPp0aUBeOxyFwS92XHpC2Q3heqZE"
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

SECRET_KEY = "8plb0vl6-HkU89IU_GMYBKZIfvVmMOIqrFzvtdA0a14"

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


site_directory = "127.0.0.1:8000"

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

fuel_95 = 58
diesel = 58