from settings import customer_db, redis_conn, site_directory
from user_actions.utils import send_email, hashing, check_model
from user_actions.jwt_op import jwt_en
from user_actions.models import Mail
import json


def register(credentials):
    if customer_db.find_one({"email": credentials.email}):
        return {"msg": "There is already an account with this email"}

    result = Requests(credentials.email).check_db()
    if result: return {"msg": "You've already sent a request"}

    rand = hashing(credentials.email)

    credentials_dict = dict(credentials)
    del credentials_dict["password_confirmation"]

    credentials_json = json.dumps(credentials_dict)
    redis_conn.set(rand, credentials_json, ex=3600)

    send_email(f"{site_directory}/request/{rand}", credentials.email)

    return {"msg": "You successfully registered"}


class Requests:
    def __init__(self, credentials):
        self.email = credentials

    def check_db(self):
        for key in redis_conn.scan_iter():
            value = redis_conn.get(key)

            value = value.decode('utf-8')
            value_dict = json.loads(value)
            if value_dict["email"] == self.email:
                return True
            else:
                continue

    def accept_request(self):
        mail = redis_conn.get(self.email)
        json_mail = json.loads(mail)

        result = check_model(json_mail, Mail)
        if result: return {"msg": "It's wrong request"}

        user = customer_db.insert_one(json.loads(mail))
        redis_conn.delete(self.email)
        return {"msg": "account registrated",
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
        else:
            return {"msg": "There is no account with this email"}

    def accept_password(self, password):
        mail = redis_conn.get(self.email)
        json_mail = json.loads(mail)
        result = check_model(json_mail, Mail)
        if result is False:
            return {"msg": "It's wrong request"}

        # Use the key "email" directly instead of self.email
        filter_query = {"email": json_mail["email"]}

        new_values = {"$set": {"password": password}}
        result = customer_db.update_one(filter_query, new_values)

        redis_conn.delete(self.email)
        return {
            "msg": "Password has been accepted",
            "cookie": jwt_en({
                "user_id": str(result.upserted_id),
                "acc_status": customer_db.find_one(filter_query)["acc_status"]
            })
        }


def login(credentials):
    user = customer_db.find_one({"email": credentials.email})
    if user["password"] == credentials.password:
        return {"msg": "You logged in",
                "cookie": jwt_en({"user_id": str(user["_id"]),
                                  "acc_status": user["acc_status"]}
                                 )
                }
    else:
        return {"msg": "Wrong credentials"}
