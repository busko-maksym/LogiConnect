from datetime import datetime

from sqlalchemy.exc import NoResultFound
from vacancies.utils import (get_coordinates, consolidate_by_points,
                             generate_intermediate_points)
from settings import (vacancies_db, filters_db, customer_db,
                      site_directory, history_db, cars_db)
from vacancies.telegram import bot
import requests
from geopy.distance import geodesic
from user_actions.utils import send_email
from concurrent.futures import ThreadPoolExecutor
from bson import ObjectId


async def create_vacancies(parametrs, token):
    status = token["acc_status"]
    if status == "business" or status == "company":
        parametrs.user_id = ObjectId(token["user_id"])
        parametrs.first_coords = get_coordinates(parametrs.location_from)
        parametrs.second_coords = get_coordinates(parametrs.location_to)
        distance = await get_distance_osrm(parametrs.first_coords, parametrs.second_coords)
        try:
            parametrs.salary_per_km = round(int(parametrs.salary_range)/int(distance), 3)
            parametrs.distance = round(distance, 1)
        except Exception:
            parametrs.salary_per_km = "Unknown"
            parametrs.distance = "Unknown"
        x = vacancies_db.insert_one(parametrs.__dict__)
        users = await get_users_vacancy(parametrs.__dict__)
        for user in users:
            await bot.send_message(chat_id=user["telegram"],
                                   text=f"Ви ідеально підходите на цю вакансію:\n{parametrs.title}"
                                        f"\n{site_directory}/vacancies/{x.inserted_id}"
                                        f"\n{parametrs.description}"
                                        f"\n{parametrs.location_from}-->{parametrs.location_to}: {parametrs.distance}km📏"
                                        f"\n{parametrs.salary_range}-->{parametrs.salary_per_km} {parametrs.currency}💸")
        return {"msg": "Registered successfully",
                "id": str(x.inserted_id)}
    else:
        return {"msg": "You don`t have right account type or creating vacancy isn`t available"}


def apply_vacancy(vacancy_id, token, suggested_price):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    try:
        applicants = [i["user_id"] for i in vacancy["applicants"]]
        if ObjectId(token["user_id"]) in applicants:
            return {"msg": "You`ve already applied to this vacancy"}
        applicants_list = vacancy["applicants"]
        applicants_list.append({"user_id": ObjectId(token["user_id"]),
                                "suggested_price": suggested_price})
        vacancies_db.update_one(
            {"_id": ObjectId(vacancy_id)},
            {
                "$set": {
                    "applicants": applicants_list,
                }
            }
        )
        return {"msg": "Applied successfully"}
    except (TypeError, KeyError):
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
        user.pop("password", None)

        if user_locations and isinstance(user_locations, list):
            for user_location in user_locations:
                try:
                    distance_km = geodesic(user_location, vacancy_location).kilometers
                except ValueError:
                    break
                if distance_km <= 30.0:
                    if user_max_weight is None or vacancy["weight"] <= user_max_weight:
                        if user_max_volume is None or vacancy["volume"] <= user_max_volume:

                            result_users.append(customer_db.find_one({"_id": ObjectId(user["user_id"])}))
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
        return {"distance is unknown"}

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


def process_vacancy(vac, vacancy, points):
    if not isinstance(vac, dict) or "first_coords" not in vac or "second_coords" not in vac:
        print(f"Invalid vacancy format: {vac}")  # Debugging
        return None

    try:
        ab_vector = [tuple(vacancy["first_coords"]), tuple(vacancy["second_coords"])]
        cd_vector = [tuple(vac["first_coords"]), tuple(vac["second_coords"])]
    except TypeError as e:
        print(f"Type error with vacancy coordinates: {e}, vacancy: {vac}")
        return None

    consolid_results = consolidate_by_points(points, ab_vector, cd_vector)

    if consolid_results[0] is None or consolid_results[1] is False:
        return None

    vac["_id"] = str(vac["_id"])
    vac["user_id"] = str(vac["user_id"])
    vac.pop("applicants", None)  # Safely remove 'applicants' if it exists

    try:
        a, b = ab_vector
        c, d = cd_vector
        vac["avg_deviation"] = get_route_length_osrm([a, c, d, b]) - vac["distance"]
    except Exception as e:
        print(f"Error calculating deviation: {e}")
        vac["avg_deviation"] = None
    print(vac)
    return vac


def consolidation_return(vacancy_id, token):
    user = customer_db.find_one({"_id": ObjectId(token["user_id"])})
    car = cars_db.find_one({"user_id": ObjectId(token["user_id"])})
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    query = {}

    if not user:
        return {"msg": "There is no user with this id in applicants"}

    if car:
        query["weight"] = {"$lt": car["weight"] - vacancy["weight"]}
        query["volume"] = {"$lt": car["volume"] - vacancy["volume"]}

    vacancies = list(vacancies_db.find(query))
    points = generate_intermediate_points(vacancy["first_coords"], vacancy["second_coords"])

    to_return = []

    # Use ThreadPoolExecutor to process vacancies in parallel
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda vac: process_vacancy(vac, vacancy, points), vacancies))

    # Filter out None results
    to_return = [vac for vac in results if vac]

    return {"msg": to_return}


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


def all_vacancies():
    vacancies = vacancies_db.find()
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


def get_route_length_osrm(coords):
    base_url = "http://router.project-osrm.org/route/v1/driving/"
    coord_string = ";".join([f"{lon},{lat}" for lat, lon in coords])
    url = f"{base_url}{coord_string}?overview=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['routes'][0]['distance'] / 1000
    else:
        raise Exception(f"Error fetching route: {response.status_code}, {response.text}")


def tender_end():
    now = datetime.now()
    results = vacancies_db.find({"end_time": {"$ne": None}})
    for obj in results:
        if obj["end_time"] <= now:
            vacancies_db.delete_one({"_id": str(obj["_id"])})
