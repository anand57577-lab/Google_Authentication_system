import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.models.password_reset import PasswordResetToken
from app.security.password_reset import (
    generate_password_reset_token,
    hash_password_reset_token,
)


def create_password_reset_token(
    db: Session,
    user_id: uuid.UUID,
) -> str:

    # Generate raw token
    raw_token = generate_password_reset_token()

    # Hash token before storing it
    token_hash = hash_password_reset_token(
        raw_token
    )

    # Set expiration time
    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.PASSWORD_RESET_EXPIRE_MINUTES
        )
    )

    # Create database record
    reset_token = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(reset_token)
    db.commit()

    # Return raw token so it can be sent through email
    return raw_token