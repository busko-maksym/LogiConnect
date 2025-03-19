from fastapi import APIRouter, Depends
from user_actions.appLogic import (register, login, Requests, preferences_create,
                                   add_car, my_acc, user_pg, beta_driver_create)
from user_actions.models import (TruckDriverCreate, BusinessOwnerCreate,
                                 TransportCompanyOwnerCreate, MainUserData, UserPreference,
                                 CarAdd, BetaDriver)
from typing import Any
from user_actions.jwt_op import verify_token

router = APIRouter()


@router.post("/register/truck")
async def user_reg(user: TruckDriverCreate):
    return register(user)


@router.post("/register/business")
async def business_reg(user: BusinessOwnerCreate):
    return register(user)


@router.post("/register/transportcompany")
async def transp_reg(user: TransportCompanyOwnerCreate):
    return register(user)


@router.post("/login")
async def login_user(user: MainUserData):
    return login(user)


@router.post("/password/reset")
async def reset_password(email: str):
    return Requests(email).password_reset_request()


@router.post("/password/{id}")
async def reset_password(id: str, password: str) -> dict[str, Any]:
    """
    Description:
    :param id:
    :param password:
    :return:
    """
    return Requests(id).accept_password(password)


@router.get("/request/{request}")
async def req(request: str):
    return Requests(request).accept_request()


@router.post("/request/telegram")
async def telegram_request(token: dict = Depends(verify_token)):
    return Requests(token).telegram_req()


@router.post("/preferences")
async def preferences(preferences_data: UserPreference, token: dict = Depends(verify_token)):
    return preferences_create(preferences_data, token)


@router.post("/car")
async def car_connect(car_data: CarAdd, token: dict = Depends(verify_token)):
    return add_car(car_data, token)


@router.get("/{user_id}")
async def user_page(user_id):
    return user_pg(user_id)


@router.get("/user/me")
async def me(token: dict = Depends(verify_token)):
    return my_acc(token)


@router.post("/beta/driver")
async def driver(driver_data: BetaDriver):
    return beta_driver_create(driver_data)