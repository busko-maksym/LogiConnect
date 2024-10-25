import pymongo
import fastapi
import redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = fastapi.FastAPI()


DATABASE_URL = "postgresql://Logistic_app:aqrevcnJa6w<?cHI~M={vcnJa6w<?cHI~M=@localhost:5432/your_database"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = pymongo.MongoClient("mongodb+srv://yanamefi:gKAE9hAGHqkVYoCm@cluster0.o22hb.mongodb.net"
                             "/?retryWrites=true&w=majority&appName=Cluster0")

# Access a specific database
user_db = client["Users_db"]
chat_db = client["Chat"]
vacancies = client["Vacancies"]

# Access a collection within the database
customer_db = user_db["customer"]
messages_db = chat_db["messages"]
user_chat_db = chat_db["chats"]
vacancies_db = vacancies["vacancies"]

SECRET_KEY = "8plb0vl6-HkU89IU_GMYBKZIfvVmMOIqrFzvtdA0a14"


redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)


site_directory = "128.0.0.1:8000"

origins = [
    "http://localhost:3000",
    "localhost:3000"
]
