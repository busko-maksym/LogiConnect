from pydantic import BaseModel
from typing import List
from app.models.vacancies import Urgency


class Mail(BaseModel):
    email: str


class UserPreference(BaseModel):
    user_id: str
    max_distance: int
    minimum_wage: float
    locations: list
    urgency: List[Urgency]


class CarAdd(BaseModel):
    waste: float
    max_volume: int
    max_weight: int
    fridge: bool


