from settings import vacancies_db, filters_db, site_directory
from bson import ObjectId
from vacancies.telegram import bot


async def create_vacancies(parametrs, token):
    if token["acc_status"] == "buisness" or "company":
        parametrs.posted_by = token["user_id"]
        x = vacancies_db.insert_one(parametrs.__dict__)
        users = get_users_vacancy(parametrs)
        print(users)
        for user in users:
            print(user)
            await bot.send_message(chat_id=user, text=f"it seems that you are ideal to apply:\n {parametrs.title}"
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
        vacancy["applicants"] = vacancy.remove("applicants")
        return dict(vacancy)
    else:
        return {"msg": "This vacancy doesn't exist"}


def all_vacancies():
    vacancies = vacancies_db.find()
    return vacancies


def get_applicants(vacancy_id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(vacancy_id)})
    if vacancy and vacancy["posted_by"] == token["user_id"]:
        applicants_list = vacancy.get("applicants", [])
        return {"list": applicants_list, "msg": "Found successfully"}
    else:
        return {"msg": "You aren`t owner of vacancy or vacancy doesn`t exist anymore"}


def delete_vac(id, token):
    vacancy = vacancies_db.find_one({"_id": ObjectId(id)})
    if token["user_id"] == vacancy["posted_by"]:
        vacancies_db.delete_one({"_id": ObjectId(id)})
        return {"msg": "Deleted successfully"}
    else:
        return {"msg": "This isn't your vacancy or this vacancy doesn`t exist"}


def get_users_vacancy(vacancy):
    query = {
        "locations": {"$in": [vacancy.location_from]},
        "minimum_wage": {"$lte": float(vacancy.salary_range)},
        "urgency": {"$in": [vacancy.urgency]}
    }

    matching_users = filters_db.find(query)
    ids = [i["telegram"] for i in matching_users]
    return ids
