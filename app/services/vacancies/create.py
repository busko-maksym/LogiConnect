from bson import ObjectId
from app.core.config import vacancies_db
from app.core.security import site_directory
from app.services.vacancies.search import get_users_vacancy
from app.services.chat.telegram import bot
from app.services.vacancies.consolidation import get_coordinates, get_route_length_osrm


async def create_vacancies(parametrs, token):
    status = token["acc_status"]
    if status == "business" or status == "company":
        parametrs.user_id = ObjectId(token["user_id"])
        parametrs.first_coords = get_coordinates(parametrs.location_from)
        parametrs.second_coords = get_coordinates(parametrs.location_to)
        distance = get_route_length_osrm([parametrs.first_coords, parametrs.second_coords])
        if distance:
            parametrs.salary_per_km = round(int(parametrs.salary_range) / int(distance), 3)
            parametrs.distance = round(distance, 1)
        else:
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
                                        f"\n{parametrs.salary_range}-->{parametrs.salary_per_km} {parametrs.currency.title()} за км💸")
        return {"msg": "Registered successfully",
                "id": str(x.inserted_id)}
    else:
        return {"msg": "You don`t have right account type or creating vacancy isn`t available"}
