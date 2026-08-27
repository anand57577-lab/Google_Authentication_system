from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from app.config import settings
from app.models.email_verification import (
    EmailVerificationToken,
)
from app.security.email_verification import (
    generate_email_verification_token,
    hash_email_verification_token,
)


def create_email_verification_token(
    db: Session,
    user_id: UUID,
) -> str:

    # Generate raw token
    raw_token = (
        generate_email_verification_token()
    )

    # Hash token for database
    token_hash = (
        hash_email_verification_token(
            raw_token
        )
    )

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=(
                settings
                .EMAIL_VERIFICATION_EXPIRE_MINUTES
            )
        )
    )

    verification_token = EmailVerificationToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(verification_token)
    db.commit()

    return raw_token

def resend_email_verification_token(
    db: Session,
    user_id: UUID,
) -> str:

    # 1. Invalidate all previous unused verification tokens
    existing_tokens = (
        db.query(EmailVerificationToken)
        .filter(
            EmailVerificationToken.user_id == user_id,
            EmailVerificationToken.used == False,
        )
        .all()
    )

    for token in existing_tokens:
        token.used = True
        token.used_at = datetime.now(timezone.utc)

    # 2. Generate a new raw token
    raw_token = generate_email_verification_token()

    # 3. Hash token before storing it
    token_hash = hash_email_verification_token(
        raw_token
    )

    # 4. Set expiry
    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.EMAIL_VERIFICATION_EXPIRE_MINUTES
        )
    )

    # 5. Create new verification token
    verification_token = EmailVerificationToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(verification_token)
    db.commit()

    # 6. Return raw token for email
    return raw_token