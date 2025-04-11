from fastapi import APIRouter, Depends
from app.services.user.user import preferences_create, add_car, user_pg, my_acc
from app.services.chat.notigication import messaging
from app.services.auth.auth import beta_transfer
from app.models.user_out import (DriverOut, BusinessOut)
from app.crud.user import find_user
from app.models.user import (UserPreference,
                             CarAdd)
from app.services.auth.jwt_op import verify_token

router = APIRouter()


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


@router.post("/beta/transfer/{id_}")
async def transfer(id_: str):
    return beta_transfer(id_)


@router.post("/message")
async def message(messages: str):
    return await messaging(messages)


@router.get("/driver/{__id}", response_model=DriverOut)
async def driver(__id: str):
    return find_user(__id)


@router.get("/business/{__id}", response_model=BusinessOut)
async def business(__id: str):
    print(find_user(__id))
    return find_user(__id)


