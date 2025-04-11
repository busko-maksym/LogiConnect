from fastapi import Depends, APIRouter, Query
from app.models.vacancies import VacancyCreate
from app.services.auth.jwt_op import verify_token
from app.services.vacancies.search import all_vacancies, user_vacancies, find_vacancy, filter_vacancies, apply_vacancy, \
    get_applicants
from app.services.vacancies.vacanies import potential_employees, vacancies_radius, accept_vacancy, delete_vac, \
    close_vacancy
from app.services.vacancies.consolidation import consolidation_return, get_route_length_osrm
from app.services.vacancies.create import create_vacancies
from typing import Optional, List
# from fastapi_utils.tasks import repeat_every

router = APIRouter()


@router.post("/create")
async def vacancies_create(vacancies: VacancyCreate, decoded_token: dict = Depends(verify_token)):
    return await create_vacancies(vacancies, decoded_token)


@router.get("/")
async def vacancies_list():
    return all_vacancies()


@router.get("/{id}")
async def get_vacancy(_id: str):
    return find_vacancy(_id)


@router.post("/{id}/apply")
async def vacancy_apply(vacancies_id: str, suggested_price: str = None, decoded_token: dict = Depends(verify_token)):
    return apply_vacancy(vacancies_id, decoded_token, suggested_price)


@router.get("/{id}/applicants")
async def get(vacancies_id: str, decoded_token: dict = Depends(verify_token)):
    return get_applicants(vacancies_id, decoded_token)


@router.delete("/{id}/delete")
async def delete(_id: str, decoded_token: dict = Depends(verify_token)):
    return delete_vac(_id, decoded_token)


@router.post("/{id}/applicants/accept")
async def applicant_accept(_id: str, user_to_apply: str, decoded_token: dict = Depends(verify_token)):
    return await accept_vacancy(_id, decoded_token, user_to_apply)


@router.post("/{id}/close")
async def close(id_: str, description: str = None, mark: float = None,
                decoded_token: dict = Depends(verify_token)):
    return close_vacancy(id_, decoded_token, mark, description)


@router.post("/{id}/applicants/potential")
async def potential(_id: str, decoded_token: dict = Depends(verify_token)):
    return await potential_employees(_id, decoded_token)


@router.post("/distance")
async def distance(start_city: str, end_city: str):
    return get_route_length_osrm([start_city, end_city])


@router.post("/radius")
async def radius(start_radius: str, decoded_token: dict = Depends(verify_token)):
    return vacancies_radius(start_radius, decoded_token)


@router.post("/{vacancies_id}/consolidation")
async def consolidate(vacancies_id: str, token: dict = Depends(verify_token)):
    return consolidation_return(vacancies_id, token)


@router.get("/vacancies")
async def get_vacancies(
    min_salary: Optional[int] = None,
    max_salary: Optional[int] = None,
    max_distance: Optional[float] = 50,  # default 50 km
    max_weight: Optional[float] = None,
    max_volume: Optional[float] = None,
    urgency: Optional[List[str]] = Query(None),
    page: Optional[int] = 1,
    token: dict = Depends(verify_token)
):
    return filter_vacancies({
        "min_salary": min_salary,
        "max_salary": max_salary,
        "max_distance": max_distance,
        "max_weight": max_weight,
        "max_volume": max_volume,
        "urgency": urgency
    }, page, token)


@router.post("/my")
async def my_vacancies(token: dict = Depends(verify_token)):
    return user_vacancies(token)


# @router.on_startup()
# @repeat_every(seconds=300)
# def check_tenders_status():
#     tender_end()
