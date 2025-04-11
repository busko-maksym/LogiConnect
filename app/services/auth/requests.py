import json

from bson import ObjectId

from app.core.config import customer_db
from app.core.security import redis_conn, site_directory
from app.models.user import Mail
from app.services.auth.jwt_op import jwt_en
from app.utils import check_model, hashing, send_email


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
