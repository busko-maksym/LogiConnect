from fastapi import Request, Depends, FastAPI, Response, APIRouter
from vacancies.models import VacancyCreate
from user_actions.jwt_op import verify_token
from vacancies.appLogic import (create_vacancies, apply_vacancy, find_vacancy,
                                all_vacancies, get_applicants, delete_vac, get_users_vacancy)

router = APIRouter()


@router.post("/create")
async def vacancys_create(vacancys: VacancyCreate, decoded_token: dict = Depends(verify_token)):
    return await create_vacancies(vacancys, decoded_token)


@router.post("/{id}/apply")
async def vacancy_apply(vacancys_id: str, decoded_token: dict = Depends(verify_token)):
    return apply_vacancy(vacancys_id, decoded_token)


@router.get("/{id}")
async def get_vacancy(_id: str):
    return find_vacancy(_id)


@router.get("/")
async def get_vacancies():
    return all_vacancies()


@router.get("/{id}/applicants")
async def get(vacancies_id: str, decoded_token: dict = Depends(verify_token)):
    return get_applicants(vacancies_id, decoded_token)


@router.delete("/{id}/delete")
async def delete(_id: str, decoded_token: dict = Depends(verify_token)):
    return delete_vac(_id, decoded_token)
