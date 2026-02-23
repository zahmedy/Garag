from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CarCreate(BaseModel):
    city: str
    district: Optional[str] = None
    make_id: int
    model_id: int
    year: int
    price_sar: int
    mileage_km: Optional[int] = None
    body_type: Optional[str] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    drivetrain: Optional[str] = None
    condition: Optional[str] = None
    color: Optional[str] = None
    title_ar: str
    description_ar: str

class CarUpdate(BaseModel):
    city: Optional[str] = None
    district: Optional[str] = None
    make_id: Optional[int] = None
    model_id: Optional[int] = None
    year: Optional[int] = None
    price_sar: Optional[int] = None
    mileage_km: Optional[int] = None
    body_type: Optional[str] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    drivetrain: Optional[str] = None
    condition: Optional[str] = None
    color: Optional[str] = None
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None

class CarOut(BaseModel):
    id: int
    status: str
    city: str
    district: Optional[str]
    make_id: int
    model_id: int
    year: int
    price_sar: int
    mileage_km: Optional[int]
    title_ar: str
    description_ar: str
    published_at: Optional[datetime]