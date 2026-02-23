from datetime import datetime
import redis
from rq import Queue
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.deps import require_admin
from app.db.session import get_session
from app.models.car import CarListing, CarStatus
from app.core.config import settings
from app.tasks.indexer import index_car_listing

router = APIRouter(prefix="/admin", tags=["admin"])

redis_conn = redis.from_url(settings.REDIS_URL)
queue = Queue("default", connection=redis_conn)

@router.post("/cars/{car_id}/approve")
def approve_car(car_id: int, session: Session = Depends(get_session), admin=Depends(require_admin)):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    if car.status != CarStatus.pending_review:
        raise HTTPException(status_code=400, detail="Only pending can be approved")

    car.status = CarStatus.active
    car.published_at = datetime.utcnow()
    car.updated_at = datetime.utcnow()
    session.add(car)
    session.commit()

    queue.enqueue(index_car_listing, car.id)
    return {"ok": True, "status": car.status.value}

@router.post("/cars/{car_id}/reject")
def reject_car(car_id: int, reason: str, session: Session = Depends(get_session), admin=Depends(require_admin)):
    car = session.exec(select(CarListing).where(CarListing.id == car_id)).first()
    if not car:
        raise HTTPException(status_code=404, detail="Not found")
    if car.status != CarStatus.pending_review:
        raise HTTPException(status_code=400, detail="Only pending can be rejected")

    car.status = CarStatus.rejected
    car.updated_at = datetime.utcnow()
    session.add(car)
    session.commit()

    queue.enqueue(index_car_listing, car.id)
    return {"ok": True, "status": car.status.value, "reason": reason}