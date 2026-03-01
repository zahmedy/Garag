from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.car import CarListing, CarStatus
from app.schemas.car import CarOut

router = APIRouter(prefix="/v1/public", tags=["public"])

@router.get("/cars/{car_id}", response_model=CarOut)
def public_car_detail(car_id: int, session: Session = Depends(get_session)):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    if car.status != CarStatus.active:
        raise HTTPException(status_code=404, detail="Not found")
    return CarOut(**car.model_dump(), status=car.status.value)