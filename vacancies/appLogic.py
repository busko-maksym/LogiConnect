from sqlalchemy.exc import NoResultFound
from vacancies.utils import (get_coordinates, consolidate_by_points,
                             generate_intermediate_points)
from settings import (vacancies_db, filters_db, customer_db,
                      site_directory, history_db, redis_conn)
from bson import ObjectId
from vacancies.telegram import bot
import requests
from geopy.distance import geodesic
import time


async def create_vacancies(parametrs, token):
    start = time.time()
    status = token["acc_status"]
    if status == "business" or status == "company":
        parametrs.user_id = token["user_id"]
        parametrs.first_coords = get_coordinates(parametrs.location_from)
        parametrs.second_coords = get_coordinates(parametrs.location_to)
        parametrs.distance = await get_distance_osrm(parametrs.first_coords, parametrs.second_coords)
        x = vacancies_db.insert_one(parametrs.__dict__)
        users = await get_users_vacancy(parametrs.__dict__)
        for user in users:
            print(user["telegram"])
            await bot.send_message(chat_id=user["telegram"],
                                   text=f"it seems that you are ideal to apply:\n {parametrs.title}"
                                        f"\n {site_directory}/vacancies/{x.inserted_id}\n"
                                        f"{parametrs.description}\n"
                                        f"{parametrs.location_from}-->{parametrs.location_to}: {parametrs.distance}km")
        end = time.time()
        print(str(end-start))
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

        if user_locations and isinstance(user_locations, list):
            for user_location in user_locations:
                print(user_location, vacancy_location)
                distance_km = geodesic(user_location, vacancy_location).kilometers
                if distance_km <= 30.0:
                    if user_max_weight is None or vacancy["weight"] <= user_max_weight:
                        if user_max_volume is None or vacancy["volume"] <= user_max_volume:
                            result_users.append(user)
                    break

    return result_users



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


async def get_distance_osrm(start_city, end_city):
    if start_city is False or end_city is False:
        return {"msg": "An unexpected error occurred"}

    if not start_city or not end_city:
        return "Could not find coordinates for one or both cities."
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{start_city[1]},{start_city[0]};{end_city[1]},{end_city[0]}"
    response = requests.get(osrm_url, params={"overview": "false"})
    data = response.json()

    if response.status_code == 200 and data.get("routes"):
        distance_meters = data["routes"][0]["distance"]
        return distance_meters / 1000
    else:
        return "Could not calculate the distance."


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


def consolidation(vacancy_id, token):
    user = customer_db.find_one({"_id": ObjectId(token["user_id"])})
    if user:
        to_return = []
        vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
        vacancies = vacancies_db.find()
        points = generate_intermediate_points(vacancy["first_coords"], vacancy["second_coords"])
        for vac in vacancies:
            consolid_results = consolidate_by_points(points, [vacancy["first_coords"], vacancy["second_coords"]],
                                                     [vac["first_coords"], vac["second_coords"]])
            if consolid_results:
                vac["_id"] = str(vac["_id"])
                to_return.append(vac)
        return to_return
    else:
        return {"msg": "There is no user with this id in applicants"}
