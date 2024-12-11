from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Urgency(str, Enum):
    very_urgent = "today"
    high_urgency = "tomorrow"
    urgent = "2 days"
    low_urgency = "3-5 days"
    not_urgent = "5 and more"


class VacancyCreate(BaseModel):
    title: str
    description: str = None
    location_from: str
    location_to: str
    salary_range: Optional[float] = None
    salary_per_km: Optional[float] = None
    user_id: str
    distance: Optional[int] = None
    first_coords: Optional[List[float]] = None
    second_coords: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    weight: Optional[int]
    volume: Optional[int]
    requirements: List[str] = None
    additional_info: Optional[str] = None
    currency: Optional[str] = None
    urgency: Optional[Urgency] = None


