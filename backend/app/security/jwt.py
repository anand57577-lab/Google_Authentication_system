from datetime import datetime, timedelta, timezone

import jwt

from app.config import settings


def create_access_token(
    user_id: str,
    role: str
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",   
        "exp": expire
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token