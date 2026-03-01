from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.user import User, UserRole
from app.core.config import settings

router = APIRouter(prefix="/v1/dev", tags=["dev"])

@router.post("/make-admin")
def make_admin(phone_e164: str, session: Session = Depends(get_session)):
    # Safety: only allow in dev
    if settings.ENV != "dev":
        raise HTTPException(status_code=404, detail="Not found")

    user = session.exec(select(User).where(User.phone_e164 == phone_e164)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = UserRole.admin
    session.add(user)
    session.commit()
    return {"ok": True, "phone_e164": user.phone_e164, "role": user.role}