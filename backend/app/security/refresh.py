import hashlib
import secrets


def generate_refresh_token() -> str:
    """
    Generate a cryptographically secure random
    refresh token.
    """

    return secrets.token_urlsafe(64)


def hash_refresh_token(token: str) -> str:
    """
    Hash a refresh token before storing it
    in the database.
    """

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()