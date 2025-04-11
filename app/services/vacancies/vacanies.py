from datetime import datetime

import requests
from bson import ObjectId
from geopy.distance import geodesic
from sqlalchemy.exc import NoResultFound

import app.services
from app.core.config import vacancies_db, customer_db, history_db
from app.core.security import site_directory
from app.services.vacancies.search import get_users_vacancy
from app.services.vacancies.consolidation import get_coordinates
from app.utils import send_email


async def potential_employees(vacancy, token):
    vacancy_obj = vacancies_db.find_one({"_id": ObjectId(vacancy)})
    try:
        if vacancy_obj["user_id"] == ObjectId(token["user_id"]):
            users = await get_users_vacancy(vacancy_obj)
            user_list = []
            for user in users:
                user["_id"] = str(user["_id"])
                del user["password"]
                user_list.append(user)
            return {"msg": user_list}
        else:
            return {"msg": "Something went wrong"}
    except NoResultFound:
        return {"msg": "No vacancy found or there is other "}


def vacancies_radius(location, token):
    user = customer_db.find_one({"_id": ObjectId(token["user_id"])})
    if user is None:
        return {"msg": "There is no user with this id in applicants"}
    coords = get_coordinates(location)
    vacancies = vacancies_db.find()
    vacancies_list = []
    for vacancy in vacancies:
        vacancy_coords = vacancy.get("first_coords")
        print(vacancy_coords)
        distance_km = geodesic(list(vacancy_coords), coords).kilometers
        if distance_km <= 30.0:
            vacancy["_id"] = str(vacancy["_id"])
            vacancies_list.append(vacancy)
    return vacancies_list


def tender_end():
    now = datetime.now()
    results = vacancies_db.find({"end_time": {"$ne": None}})
    for obj in results:
        if obj["end_time"] <= now:
            vacancies_db.update_one(obj, {"$set": {"show": False}})
        else:
            pass


async def accept_vacancy(id_, token, user_to_apply):
    vacancy = vacancies_db.find_one({"_id": ObjectId(id_)})
    if vacancy is None:
        return {"msg": "This vacancy doesn't exist"}

    if vacancy["user_id"] != ObjectId(token["user_id"]):
        return {"msg": "it is not your vacancy"}

    applicants_list = vacancy["applicants"]

    if ObjectId(user_to_apply) in applicants_list:
        applicant = customer_db.find_one({"_id": ObjectId(user_to_apply)})
        vacancy["last_id"] = vacancy["_id"]
        vacancy["completed"] = False
        vacancy["completed_by"] = ObjectId(user_to_apply)
        del vacancy["_id"]
        del vacancy["applicants"]
        vac = history_db.insert_one(vacancy)
        try:
            await app.services.chat.chat.send_message(chat_id=applicant["telegram"], text=f"You've been accepted to this vacancy: "
                                                                 f"{site_directory}/vacancies/history/{vac.inserted_id}"
                                                                 f"\n you can write to owner of vacancy:"
                                                                 f"{site_directory}/chat/create/{vacancy["user_id"]}")
        except (NameError, KeyError):
            send_email(f"You've been accepted to this vacancy: "
                             f"{site_directory}/vacancies/history/{vac.inserted_id}"
                             f"\n you can write to owner of vacancy:"
                             f"{site_directory}/chat/create/{vacancy["user_id"]}", applicant["email"])
        vacancies_db.delete_one({"_id": ObjectId(id_)})
        return {"msg": "You accepted user on vacancy"}
    else:
        return {"msg": "There is no user with this id in applicants"}


def delete_vac(id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(id)})
    if ObjectId(token["user_id"]) == vacancy["user_id"]:
        vacancies_db.delete_one({"_id": ObjectId(id)})
        return {"msg": "Deleted successfully"}
    else:
        return {"msg": "This isn't your vacancy or this vacancy doesn`t exist"}


def close_vacancy(id_, token, mark, description):
    vacancy = history_db.find_one({"last_id": ObjectId(id_), "completed": False})
    if vacancy is None:
        return {"msg": "This vacancy doesn't exist"}
    user = customer_db.find_one({"_id": ObjectId(vacancy["completed_by"])})
    if vacancy["user_id"] != ObjectId(token["user_id"]):
        return {"msg": "it is not your vacancy"}
    complicant = customer_db.find_one({"_id": ObjectId(vacancy["completed_by"])})
    customer_db.update_one({complicant, {"$push": {"marks": {"mark": str(mark),
                                                             "description": description}}}})
    avg_mark = (complicant["avg_mark"]*len(complicant["marks"])+mark)/(len(complicant["marks"])+1)
    customer_db.update_one({complicant, {"$set": {"avg_mark": avg_mark}}})
    history_db.update_one({"last_id": ObjectId(id_)},
                          {
                              "$set": {
                                  "completed": True,
                              }
                          })
    send_email(f"Hello, your vacancy named {vacancy['title']}", user["email"])
    return {"msg": "Vacancy closed"}
