from fastapi import APIRouter, Depends
from app.services.auth.requests import Requests
from app.services.auth.auth import register, login, beta_driver_create
from app.models.auth import TruckDriverCreate, BusinessOwnerCreate, TransportCompanyOwnerCreate, MainUserData, \
    BetaDriver
from typing import Any
from app.services.auth.jwt_op import verify_token

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


@router.post("/beta/driver")
async def driver(driver_data: BetaDriver):
    return beta_driver_create(driver_data)


