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
    salary_range: Optional[str] = None
    posted_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    requirements: List[str] = None
    additional_info: Optional[str] = None
    currency: Optional[str] = None
    urgency: Optional[Urgency] = None


