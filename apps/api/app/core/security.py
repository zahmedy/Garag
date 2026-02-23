from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from app.core.config import settings

ALGORITHM = "HS256"

def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    exp = datetime.utcnow() + timedelta(minutes=expires_minutes or settings.JWT_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": exp}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)

def decode_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None