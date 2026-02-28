from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.schemas.auth import OTPRequest, OTPVerify, TokenResponse
from app.db.session import get_session
from app.models.user import User, UserRole
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/request-otp")
def request_otp(payload: OTPRequest):
    # MVP: no-op. In prod: send OTP using Twilio Verify or local SMS provider.
    return {"ok": True}

@router.post("/verify-otp", response_model=TokenResponse)
def verify_otp(payload: OTPVerify, session: Session = Depends(get_session)):
    if payload.code != "0000":
        raise HTTPException(status_code=400, detail="Invalid code (MVP accepts 0000)")

    user = session.exec(select(User).where(User.phone_e164 == payload.phone_e164)).first()
    if not user:
        user = User(phone_e164=payload.phone_e164, role=UserRole.seller, verified_at=datetime.utcnow())
        session.add(user)
        session.commit()
        session.refresh(user)
    else:
        if user.is_banned:
            raise HTTPException(status_code=403, detail="User is banned")
        if not user.verified_at:
            user.verified_at = datetime.utcnow()
            session.add(user)
            session.commit()

    token = create_access_token(subject=str(user.id))
    return TokenResponse(access_token=token)
