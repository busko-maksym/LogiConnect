from sqlalchemy.exc import NoResultFound
from vacancies.utils import get_coordinates
from settings import (vacancies_db, filters_db, customer_db,
                      site_directory, history_db, redis_conn)
from bson import ObjectId
from vacancies.telegram import bot
import requests


async def create_vacancies(parametrs, token):
    status = token["acc_status"]
    if status == "business" or status == "company":
        parametrs.user_id = token["user_id"]
        parametrs.distance = get_distance_osrm(parametrs.location_from, parametrs.location_to)
        x = vacancies_db.insert_one(parametrs.__dict__)
        users = get_users_vacancy(parametrs.__dict__)
        for user in users:
            await bot.send_message(chat_id=user["telegram"],
                                   text=f"it seems that you are ideal to apply:\n {parametrs.title}"
                                        f"\n {site_directory}/vacancies/{x.inserted_id}\n"
                                        f"{parametrs.description}\n"
                                        f"{parametrs.location_from}-{parametrs.location_to}")
        return {"msg": "Registered successfully",
                "id": str(x.inserted_id)}
    else:
        return {"msg": "You don`t have right account type or creating vacancy isn`t available"}


def apply_vacancy(vacancy_id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})

    if vacancy:
        applicants_list = vacancy.get("applicants", [])
        applicants_list.append(token["user_id"])

        vacancies_db.update_one(
            {"_id": ObjectId(vacancy_id)},
            {
                "$set": {
                    "applicants": applicants_list,
                }
            }
        )
        return {"msg": "Applied successfully"}
    else:
        return {"msg": "This vacancy doesn't exist"}


def find_vacancy(_id):
    vacancy = vacancies_db.find_one({"_id": ObjectId(_id)})

    if vacancy:
        vacancy["_id"] = str(vacancy["_id"])
        return dict(vacancy)
    else:
        return {"msg": "This vacancy doesn't exist"}


def all_vacancies():
    vacancies = vacancies_db.find()
    list_vacancies = []

    for vacancy in vacancies:
        vacancy["_id"] = str(vacancy["_id"])
        vacancy["user_id"] = str(vacancy["user_id"])
        list_vacancies.append(vacancy)

    return {"msg": list_vacancies}


def get_applicants(vacancy_id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    if vacancy and vacancy["user_id"] == token["user_id"]:
        applicants_list = vacancy.get("applicants", [])
        return {"list": applicants_list, "msg": "Found successfully"}
    else:
        return {"msg": "You aren`t owner of vacancy or vacancy does not exist anymore"}


def delete_vac(id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(id)})
    if token["user_id"] == vacancy["posted_by"]:
        vacancies_db.delete_one({"_id": ObjectId(id)})
        return {"msg": "Deleted successfully"}
    else:
        return {"msg": "This isn't your vacancy or this vacancy doesn`t exist"}


def get_users_vacancy(vacancy):
    query = {
        "locations": {"$in": [vacancy["location_from"]]},
        "minimum_wage": {"$lte": float(vacancy["salary_range"])},
        "urgency": {"$in": [vacancy["urgency"]]}
    }

    matching_users = filters_db.find(query)
    users = [user for user in matching_users]
    return users


def accept_vacancy(id_, token, user_to_apply):
    vacancy = vacancies_db.find_one({"_id": ObjectId(id_)})
    if vacancy["user_id"] != token["user_id"]:
        return {"msg": "it is not your vacancy"}
    applicants_list = vacancy["applicants"]
    if user_to_apply in applicants_list:
        vacancy["last_id"] = str(vacancy["_id"])
        vacancy["vacancy_status"] = "In work"
        vacancy["completed_by"] = user_to_apply
        history_db.insert_one(vacancy)
        vacancies_db.delete_one({"_id": id_})
        return {"msg": "You accepted user on vacancy"}
    else:
        return {"msg": "There is no user with this id in applicants"}


def close_vacancy(id_, token, mark, description):
    vacancy = history_db.find_one({"last_id": id_})
    if vacancy["user_id"] != token["user_id"]:
        return {"msg": "it is not your vacancy"}
    customer_db.update_one({"_id": ObjectId(vacancy["completed_by"])}, {"$addToSet": {"marks": mark}})
    customer_db.update_one({"_id": ObjectId(vacancy["completed_by"])}, {"$addToSet": {"description": description}})
    history_db.update_one({"_id": ObjectId(id_)},
                          {
                              "$set": {
                                  "vacancy_status": "Completed",
                              }
                          })
    return {"msg": "Vacancy closed"}


def potential_emloyees(vacancy, token):
    vacancy_obj = vacancies_db.find_one({"_id": ObjectId(vacancy)})
    try:
        if vacancy_obj["user_id"] == token["user_id"]:
            users = get_users_vacancy(vacancy_obj)
            user_list = []
            for user in users:
                user["_id"] = str(user["_id"])
                user_list.append(user)
            return {"msg": user_list}
        else:
            return {"msg": "Something went wrong"}
    except NoResultFound:
        return {"msg": "No vacancy found or there is other "}


def get_distance_osrm(start_city, end_city):
    start_coords = get_coordinates(start_city)
    end_coords = get_coordinates(end_city)

    if start_coords is False or end_coords is False:
        return {"msg": "An unexpected error occurred"}

    if not start_coords or not end_coords:
        return "Could not find coordinates for one or both cities."

    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}"
    response = requests.get(osrm_url, params={"overview": "false"})
    data = response.json()

    if response.status_code == 200 and data.get("routes"):
        distance_meters = data["routes"][0]["distance"]
        return distance_meters / 1000
    else:
        return "Could not calculate the distance."


