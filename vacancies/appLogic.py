from sqlalchemy.exc import NoResultFound
from vacancies.utils import (get_coordinates, consolidate_by_points,
                             generate_intermediate_points)
from settings import (vacancies_db, filters_db, customer_db,
                      site_directory, history_db, cars_db)
from bson import ObjectId
from vacancies.telegram import bot
import requests
from geopy.distance import geodesic
from user_actions.utils import send_email


async def create_vacancies(parametrs, token):
    status = token["acc_status"]
    if status == "business" or status == "company":
        parametrs.user_id = ObjectId(token["user_id"])
        parametrs.first_coords = get_coordinates(parametrs.location_from)
        parametrs.second_coords = get_coordinates(parametrs.location_to)
        distance = await get_distance_osrm(parametrs.first_coords, parametrs.second_coords)
        parametrs.salary_per_km = round(parametrs.salary_range / distance, 3)
        parametrs.distance = round(distance, 1)
        x = vacancies_db.insert_one(parametrs.__dict__)
        users = await get_users_vacancy(parametrs.__dict__)
        for user in users:
            print(user["telegram"])
            await bot.send_message(chat_id=user["telegram"],
                                   text=f"it seems that you are ideal to apply:\n {parametrs.title}"
                                        f"\n{site_directory}/vacancies/{x.inserted_id}"
                                        f"\n{parametrs.description}"
                                        f"\n{parametrs.location_from}-->{parametrs.location_to}: {parametrs.distance}km📏"
                                        f"\n{parametrs.salary_range}-->{parametrs.salary_range} {parametrs.currency}💸")
        return {"msg": "Registered successfully",
                "id": str(x.inserted_id)}
    else:
        return {"msg": "You don`t have right account type or creating vacancy isn`t available"}


def apply_vacancy(vacancy_id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    try:
        if ObjectId(token["user_id"]) in vacancy["applicants"]:
            return {"msg": "You`ve already applied to this vacancy"}
        applicants_list = vacancy["applicants"]
        applicants_list.append(ObjectId(token["user_id"]))

        vacancies_db.update_one(
            {"_id": ObjectId(vacancy_id)},
            {
                "$set": {
                    "applicants": applicants_list,
                }
            }
        )
        return {"msg": "Applied successfully"}
    except TypeError:
        return {"msg": "This vacancy doesn't exist"}


def find_vacancy(_id):
    vacancy = vacancies_db.find_one({"_id": ObjectId(_id)})

    if vacancy:
        vacancy["user_id"] = str(vacancy["user_id"])
        vacancy["_id"] = str(vacancy["_id"])
        del vacancy["applicants"]
        return dict(vacancy)
    else:
        return {"msg": "This vacancy doesn't exist"}


def get_applicants(vacancy_id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    if vacancy and vacancy["user_id"] == ObjectId(token["user_id"]):
        applicants_list = vacancy.get("applicants", [])
        lst = []
        for i in applicants_list:
            user = customer_db.find_one({"_id": ObjectId(i)})
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


def delete_vac(id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(id)})
    if ObjectId(token["user_id"]) == vacancy["user_id"]:
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
        del user["password"]

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
            await bot.send_message(chat_id=applicant["telegram"], text=f"You've been accepted to this vacancy: "
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


def close_vacancy(id_, token, mark, description):
    vacancy = history_db.find_one({"last_id": ObjectId(id_), "completed": False})
    if vacancy is None:
        return {"msg": "This vacancy doesn't exist"}
    user = customer_db.find_one({"_id": ObjectId(vacancy["completed_by"])})
    if vacancy["user_id"] != ObjectId(token["user_id"]):
        return {"msg": "it is not your vacancy"}
    customer_db.update_one({"_id": vacancy["completed_by"]}, {"$set": {"marks": {str(mark): description}}})
    history_db.update_one({"last_id": ObjectId(id_)},
                          {
                              "$set": {
                                  "completed": True,
                              }
                          })
    send_email(f"Hello, your vacancy named {vacancy['title']}", user["email"])
    return {"msg": "Vacancy closed"}


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
            ab_vector = [vacancy["first_coords"], vacancy["second_coords"]]
            cd_vector = [vac["first_coords"], vac["second_coords"]]
            consolid_results = consolidate_by_points(points, ab_vector,
                                                     cd_vector)
            if consolid_results:
                vac["_id"] = str(vac["_id"])
                vac["avg_deviation"] = min(geodesic(actual, planned).km)
                to_return.append(vac)
        return to_return
    else:
        return {"msg": "There is no user with this id in applicants"}


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
