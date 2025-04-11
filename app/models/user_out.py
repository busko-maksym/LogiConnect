from datetime import datetime
from pydantic import BaseModel
from typing import List


class UserDefault(BaseModel):
    _id: str
    first_name: str
    last_name: str
    email: str
    marks: dict = None
    register_date: datetime = None
    telegram: int = None


class DriverOut(UserDefault):
    driver_license_type: list = []
    driver_license_number: str
    experience_years: int = None
    vehicle_types: list = []
    has_international_permit: bool = False


class BusinessOut(UserDefault):
    company_name: str
    business_type: str
    company_size: int
    logistics_frequency: str
    cargo_types: list = None
