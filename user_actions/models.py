from pydantic import BaseModel, model_validator
from typing import List, Optional
from enum import Enum
from vacancies.models import Urgency


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    marks: list = []


class DriverLicenseType(str, Enum):

    A = "A"
    A_ = "A1"
    B = "B"
    B_ = "B1"
    C = "C"
    С_ = "C1"
    D = "D"
    D_ = "D1"


class TruckDriverCreate(UserBase):
    acc_status: str = "driver"
    driver_license_type: List[DriverLicenseType] = []
    driver_license_number: str
    experience_years: int = None
    vehicle_types: List[str] = []
    has_international_permit: bool = False


class BusinessOwnerCreate(UserBase):
    acc_status: str = "business"
    company_name: str
    business_type: str
    company_size: int
    logistics_frequency: str
    cargo_types: List[str]


class TransportCompanyOwnerCreate(UserBase):
    acc_status: str = "company"
    company_name: str
    fleet_size: int
    vehicle_types: List[str]
    operation_area: str
    special_permits: Optional[List[str]] = None


class MainUserData(BaseModel):
    email: str
    password: str


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
