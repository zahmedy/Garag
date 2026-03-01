from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import require_admin
from app.db.session import get_session
from app.models.car import CarListing, CarStatus

router = APIRouter(prefix="/v1/admin", tags=["admin"])


@router.post("/cars/{car_id}/approve")
def approve_car(
    car_id: int,
    session: Session = Depends(get_session),
    admin=Depends(require_admin),
):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    if car.status != CarStatus.pending_review:
        raise HTTPException(status_code=400, detail="Only pending_review can be approved")

    car.status = CarStatus.active
    car.published_at = datetime.utcnow()
    car.updated_at = datetime.utcnow()

    session.add(car)
    session.commit()
    return {"ok": True, "status": car.status.value, "published_at": car.published_at}


@router.post("/cars/{car_id}/reject")
def reject_car(
    car_id: int,
    reason: str,
    session: Session = Depends(get_session),
    admin=Depends(require_admin),
):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    if car.status != CarStatus.pending_review:
        raise HTTPException(status_code=400, detail="Only pending_review can be rejected")

    car.status = CarStatus.rejected
    car.updated_at = datetime.utcnow()
    session.add(car)
    session.commit()
    return {"ok": True, "status": car.status.value, "reason": reason}