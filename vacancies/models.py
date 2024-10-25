from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class VacancyBase(BaseModel):
    title: str
    description: str
    location_from: str
    location_to: str
    salary_range: Optional[str] = None
    posted_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class VacancyCreate(VacancyBase):
    requirements: List[str]
    additional_info: Optional[str] = None
    money_per_hour: Optional[float] = None
    currency: Optional[str] = None
