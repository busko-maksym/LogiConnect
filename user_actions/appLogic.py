from settings import customer_db, redis_conn, site_directory, filters_db, cars_db, beta_users
from user_actions.utils import send_email, hashing, check_model
from vacancies.appLogic import get_coordinates
from user_actions.jwt_op import jwt_en
from user_actions.models import Mail
import json
from bson import ObjectId
from vacancies.telegram import bot

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


class Requests:
    def __init__(self, credentials):
        self.email = credentials

    def check_db(self):
        for key in redis_conn.scan_iter():
            value = redis_conn.get(key)

            value = value.encode('utf-8')
            value_dict = json.loads(value)
            if value_dict["email"] == self.email:
                return True
            else:
                continue

    def accept_request(self):
        mail = redis_conn.get(self.email)
        try:
            json_mail = json.loads(mail)
        except TypeError:
            return {"msg": "Something went wrong... But it seems that link is expired"}
        result = check_model(json_mail, Mail)
        if result is None: return {"msg": "It's wrong request"}

        user = customer_db.insert_one(json.loads(mail))
        redis_conn.delete(self.email)
        return {"msg": "account registered",
                "cookie": jwt_en({"user_id": str(user.inserted_id),
                                  "acc_status": json_mail["acc_status"]}
                                 )}

    def password_reset_request(self):
        user = customer_db.find_one({"email": self.email})
        if user:
            result = Requests(self.email).check_db()
            if result: return {"msg": "You've already sent a request"}
            hashed_user = hashing(user["email"])
            credentials_json = json.dumps({"email": self.email})
            redis_conn.set(hashed_user, credentials_json, ex=3600)
            send_email(f"{site_directory}/user/password/{hashed_user}", self.email)
            return {"msg": "Please, check your email for a link"}
        else:
            return {"msg": "There is no account with this email"}

    def accept_password(self, password):
        mail = redis_conn.get(self.email)
        try:
            json_mail = json.loads(mail)
        except TypeError:
            return {"msg": "Something went wrong... But it seems that link is expired"}

        result = check_model(json_mail, Mail)
        if result is False:
            return {"msg": "It's wrong request"}

        # Use the key "email" directly instead of self.email
        filter_query = {"email": json_mail["email"]}

        new_values = {"$set": {"password": hashing(password)}}
        customer_db.update_one(filter_query, new_values)
        user = customer_db.find_one(filter_query)
        redis_conn.delete(self.email)
        return {
            "msg": "Password has been accepted",
            "cookie": jwt_en({
                "user_id": str(user["_id"]),
                "acc_status": user["acc_status"]
            })
        }

    def telegram_req(self):
        user = customer_db.find_one({"_id": ObjectId(self.email["user_id"])})
        result = Requests(user["email"]).check_db()
        if result: return {"msg": "You've already sent a request"}
        hashed_user = hashing(user["email"])
        credentials_json = json.dumps({"email": user["email"]})
        redis_conn.set(hashed_user, credentials_json, ex=10800)
        return {"msg": "You succesfully sent request, now go to link",
                "link": f"t.me/LogiConnect_bot?start=connect-{hashed_user}"}


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


def preferences_create(credentials, token):
    id_ = token["user_id"]
    user = customer_db.find_one({"_id": ObjectId(id_)})
    if token["acc_status"] != "driver":
        return {"msg": "This feature is made for drivers only"}

    if user["telegram"] is None:
        return {"msg": "At first, you have to add telegram to your account"}

    dict_credentials = dict(credentials)
    dict_credentials["locations"] = [get_coordinates(loc) for loc in dict_credentials["locations"]]
    dict_credentials["user_id"] = ObjectId(id_)
    dict_credentials["telegram"] = user["telegram"]
    if filters_db.find_one({"user_id": ObjectId(id_)}):
        filters_db.update_one({"user_id": ObjectId(id_)}, {"$set": dict_credentials})
        return {"msg": "Your preferences have been created"}
    filters_db.insert_one(dict_credentials)
    return {"msg": "Your preferences have been created"}


def add_car(params, token):
    car = cars_db.find({"user_id": ObjectId})
    params_dict = params.__dict__
    filter_obj = filters_db.find_one({"user_id": ObjectId(token["user_id"])})
    params_dict["user_id"] = ObjectId(token["user_id"])
    query = {}
    for k, v in params.items():
        if v is not None:
            query[k] = v

    if car:
        cars_db.delete_one({"user_id": ObjectId(token["user_id"])})
        cars_db.insert_one(params_dict)

    else:
        cars_db.insert_one(params_dict)

    if filter_obj is None:
        filters_db.insert_one({"volume": params_dict["volume"],
                               "weight": params_dict["weight"],
                               "user_id": ObjectId(token["user_id"])})
    else:
        filters_db.update_one({"user_id": ObjectId(token["user_id"])},
                              {"$set": {"max_volume": params_dict["max_volume"],
                                        "max_weight": params_dict["max_weight"]}})

    return {"msg": "Your car have been added"}


def user_pg(id_):
    user = customer_db.find_one({"_id": ObjectId(id_)})
    user["_id"] = str(user["_id"])
    del user["password"]
    return user


def my_acc(token):
    user = customer_db.find_one({"_id": ObjectId(token["user_id"])})
    user["_id"] = str(user["_id"])
    del user["password"]
    return user


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


async def messaging(message):
    users = list(beta_users.find())  # Convert cursor to list
    for user in users:
        try:
            await bot.send_message(user["telegram"], message)
        except Exception:
            send_email(message, user["email"])

    return {"msg": "Your message has been sent"}
