from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import get_current_user
from app.db.session import get_session
from app.models.car import CarListing, CarStatus
from app.schemas.car import CarCreate, CarUpdate, CarOut
from app.models.user import User

router = APIRouter(prefix="/cars", tags=["cars"])

def ensure_owner(car: CarListing, user: User):
    if car.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not your listing")

@router.post("", response_model=CarOut)
def create_car(payload: CarCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    car = CarListing(
        owner_id=user.id,
        status=CarStatus.draft,
        **payload.model_dump(),
    )
    session.add(car)
    session.commit()
    session.refresh(car)
    return CarOut(**car.model_dump())

@router.patch("/{car_id}", response_model=CarOut)
def update_car(car_id: int, payload: CarUpdate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    ensure_owner(car, user)

    if car.status not in [CarStatus.draft, CarStatus.pending_review]:
        raise HTTPException(status_code=400, detail="Only draft/pending can be edited")

    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(car, k, v)
    car.updated_at = datetime.utcnow()

    session.add(car)
    session.commit()
    session.refresh(car)
    return CarOut(**car.model_dump())

@router.post("/{car_id}/submit", response_model=CarOut)
def submit_car(car_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    ensure_owner(car, user)

    if car.status != CarStatus.draft:
        raise HTTPException(status_code=400, detail="Only draft can be submitted")

    # MVP quality gates (add more later)
    if car.price_sar <= 0 or car.year < 1980:
        raise HTTPException(status_code=400, detail="Invalid price/year")

    car.status = CarStatus.pending_review
    car.updated_at = datetime.utcnow()

    session.add(car)
    session.commit()
    session.refresh(car)
    return CarOut(**car.model_dump())

@router.post("/{car_id}/mark-sold", response_model=CarOut)
def mark_sold(car_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    ensure_owner(car, user)

    if car.status != CarStatus.active:
        raise HTTPException(status_code=400, detail="Only active can be sold")

    car.status = CarStatus.sold
    car.updated_at = datetime.utcnow()

    session.add(car)
    session.commit()
    session.refresh(car)
    return CarOut(**car.model_dump())