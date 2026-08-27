import hashlib
import secrets


def generate_email_verification_token() -> str:
    """
    Generate a secure random email verification token.
    """

    return secrets.token_urlsafe(48)


def hash_email_verification_token(
    token: str
) -> str:
    """
    Hash the verification token before
    storing it in PostgreSQL.
    """

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()