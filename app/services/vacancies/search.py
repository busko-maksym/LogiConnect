from bson import ObjectId
from geopy.distance import geodesic

from app.core.config import vacancies_db, history_db, cars_db, customer_db, filters_db


def all_vacancies():
    vacancies = vacancies_db.find({"show": True})
    list_vacancies = []

    for vacancy in vacancies:
        vacancy["_id"] = str(vacancy["_id"])
        vacancy["user_id"] = str(vacancy["user_id"])
        if "applicants" in vacancy:
            del vacancy["applicants"]  # Safely delete "applicants" from the vacancy document
        list_vacancies.append(vacancy)

    return {"msg": list_vacancies}


def user_vacancies(token):
    # Helper function to fetch and clean cursor data
    def fetch_and_clean(cursor):
        lst = []
        for vac in cursor:
            dict_vac = dict(vac)
            dict_vac["_id"] = str(dict_vac["_id"])
            dict_vac["user_id"] = str(dict_vac["user_id"])
            dict_vac["completed_by"] = str(dict_vac.get("completed_by", ""))  # Safe retrieval
            dict_vac["last_id"] = str(dict_vac.get("last_id", ""))  # Safe retrieval
            try:
                del dict_vac["applicants"]
            except KeyError:
                continue
            lst.append(dict_vac)
        return lst

    user_id = ObjectId(token["user_id"])

    if token["acc_status"] == "driver":
        vac_list = fetch_and_clean(history_db.find({"completed_by": user_id}))
    else:
        user_vacancies = fetch_and_clean(vacancies_db.find({"user_id": user_id}))
        history_vacancies = fetch_and_clean(history_db.find({"user_id": user_id}))
        vac_list = user_vacancies + history_vacancies

    return vac_list


def find_vacancy(_id):
    vacancy = vacancies_db.find_one({"_id": ObjectId(_id)})

    if vacancy:
        vacancy["user_id"] = str(vacancy["user_id"])
        vacancy["_id"] = str(vacancy["_id"])
        del vacancy["applicants"]
        return dict(vacancy)
    else:
        return {"msg": "This vacancy doesn't exist"}


def filter_vacancies(filters, page, token):
    filters_query = {}
    for k, v in filters.items():
        if v:
            filters_query[k] = v
        else:
            continue
    results = [obj for obj in vacancies_db.find(filters).skip((page-1) * 10).limit(10)]
    car = cars_db.find_one({'user_id': ObjectId(token["user_id"])})
    if car is None:
        return {"msg": "No data, you have to add your car"}

    for obj in results:
        obj["real_price"] = (car["waste"]+obj["weight"]*0.0013)
        obj["_id"] = str(obj["_id"])
    return {"vacancies": results}


def apply_vacancy(vacancy_id, token, suggested_price):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    try:
        applicants = [i["user_id"] for i in vacancy["applicants"]]
        if ObjectId(token["user_id"]) in applicants:
            return {"msg": "You`ve already applied to this vacancy"}
        applicants_list = vacancy["applicants"]
        applicants_list.append({"user_id": ObjectId(token["user_id"]),
                                "suggested_price": suggested_price})
        vacancies_db.update_one({vacancy, {"$push": {"applicants": applicants_list}}})
        return {"msg": "Applied successfully"}
    except (TypeError, KeyError):
        return {"msg": "This vacancy doesn't exist"}


def get_applicants(vacancy_id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    if vacancy and vacancy["user_id"] == ObjectId(token["user_id"]):
        applicants_list = vacancy.get("applicants", [])
        lst = []
        for i in applicants_list:
            user = customer_db.find_one({"_id": ObjectId(i["user_id"])})
            user["_id"] = str(user["_id"])

            try:
                marks_list = [mark for mark, desc in user["marks"].items]
                user["avg_mark"] = round(sum(marks_list) / len(marks_list), 2)
            except TypeError:
                user["avg_mark"] = None

            del user["password"]
            lst.append(user)
        return {"list": lst, "msg": "Found successfully"}
    else:
        return {"msg": "You aren`t owner of vacancy or vacancy does not exist anymore"}


async def get_users_vacancy(vacancy):
    query = {
        "minimum_wage": {"$lte": float(vacancy["salary_range"])},
        "urgency": {"$in": [vacancy["urgency"]]}
    }

    matching_users = list(filters_db.find(query))
    if not matching_users:
        return []

    result_users = []
    vacancy_location = vacancy["first_coords"]

    for user in matching_users:
        user_locations = user.get("locations", [])
        user_max_weight = user.get("max_weight", None)
        user_max_volume = user.get("max_volume", None)
        user.pop("password", None)

        if user_locations and isinstance(user_locations, list):
            for user_location in user_locations:
                try:
                    distance_km = geodesic(user_location, vacancy_location).kilometers
                except ValueError:
                    break
                if distance_km <= 50.0:
                    if user_max_weight is None or vacancy["weight"] <= user_max_weight:
                        if user_max_volume is None or vacancy["volume"] <= user_max_volume:

                            result_users.append(customer_db.find_one({"_id": ObjectId(user["user_id"])}))
                    break
    return result_users
