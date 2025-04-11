import os

import pymongo
import redis

client = pymongo.MongoClient("mongodb+srv://yanamefi:gKAE9hAGHqkVYoCm@cluster0.o22hb.mongodb.net"
                             "/?retryWrites=true&w=majority&appName=Cluster0")
TOKEN = "7835528925:AAEEayAqPp0aUBeOxyFwS92XHpC2Q3heqZE"
SECRET_KEY = "8plb0vl6-HkU89IU_GMYBKZIfvVmMOIqrFzvtdA0a14"
REDIS_URL = os.getenv("REDIS_URL", "redis://default:wEQHCtEneqIJFCxPUyFulvqQccgbAbVu@gondola.proxy.rlwy.net:33419")
redis_conn = redis.from_url(REDIS_URL, decode_responses=True)
site_directory = "appealing-beauty-production.up.railway.app"
origins = [
    "http://localhost:3000",
    "localhost:3000"
]
