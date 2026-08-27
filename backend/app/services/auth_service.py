from sqlalchemy.orm import Session

from app.models.user import User
from app.security.password import (
    verify_password,
)


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return None

    if not user.password_hash:
        return None

    password_valid = verify_password(
        password,
        user.password_hash
    )

    if not password_valid:
        return None

    return user