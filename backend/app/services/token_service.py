from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.config import settings
from app.models.refresh_token import RefreshToken
from app.security.refresh import (
    generate_refresh_token,
    hash_refresh_token,
)


def create_refresh_token(
    db: Session,
    user_id: UUID,
) -> str:

    # Generate random token
    raw_token = generate_refresh_token()

    # Hash token for database storage
    token_hash = hash_refresh_token(
        raw_token
    )

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
    )

    refresh_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(refresh_token)
    db.commit()

    return raw_token


def get_refresh_token(
    db: Session,
    raw_token: str,
):
    token_hash = hash_refresh_token(
        raw_token
    )

    refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token_hash == token_hash
        )
        .first()
    )

    return refresh_token


def revoke_refresh_token(
    db: Session,
    refresh_token: RefreshToken,
):
    refresh_token.revoked = True

    refresh_token.revoked_at = (
        datetime.now(timezone.utc)
    )

    db.commit()