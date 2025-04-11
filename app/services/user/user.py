from bson import ObjectId

from app.core.config import customer_db, filters_db, cars_db
from app.services.vacancies.consolidation import get_coordinates


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
