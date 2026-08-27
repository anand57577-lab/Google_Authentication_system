import hashlib
import secrets


def generate_password_reset_token() -> str:
    """
    Generate a cryptographically secure random password reset token.
    """

    return secrets.token_urlsafe(32)


def hash_password_reset_token(token: str) -> str:
    """
    Hash the raw password reset token using SHA-256.

    Only this hash should be stored in the database.
    """

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()