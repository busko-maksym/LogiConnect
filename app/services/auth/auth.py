import json

from bson import ObjectId

from app.core.config import customer_db, beta_users
from app.core.security import redis_conn, site_directory
from app.services.auth.jwt_op import jwt_en
from app.utils import hashing, send_email
from app.services.auth.requests import Requests


def register(credentials):
    if customer_db.find_one({"email": credentials.email}):
        return {"msg": "There is already an account with this email"}

    result = Requests(credentials.email).check_db()
    if result: return {"msg": "You've already sent a request"}

    rand = hashing(credentials.email)

    credentials_dict = dict(credentials)
    credentials_dict["password"] = hashing(credentials_dict["password"])

    credentials_json = json.dumps(credentials_dict)

    redis_conn.set(rand, credentials_json, ex=3600)

    send_email(f"{site_directory}/user/request/{rand}", credentials.email)

    return {"msg": "You successfully registered"}


def login(credentials):
    user = customer_db.find_one({"email": credentials.email})
    if user["password"] == hashing(credentials.password):
        return {"msg": "You logged in",
                "cookie": jwt_en({"user_id": str(user["_id"]),
                                  "acc_status": user["acc_status"]}
                                 )
                }
    else:
        return {"msg": "Wrong credentials"}


def beta_driver_create(data):
    users_list = beta_users.find_one({"email": data.email})
    if users_list:
        return {"msg": "You've already sent a request"}
    user = beta_users.insert_one(data.__dict__)
    send_email("you applied for beta-test of LogiConnect. Thank you for your time, "
               "when we will release, you will be first to hear about that!"
               "we will be very happy if you had connected telegram "
               f"t.me/LogiConnect_bot?start=beta-{str(user.inserted_id)}", data.email)
    return {"link": f"t.me/LogiConnect_bot?start=beta-{str(user.inserted_id)}"}


def beta_transfer(id_):
    return beta_users.find_one({"_id": ObjectId(id_)})
