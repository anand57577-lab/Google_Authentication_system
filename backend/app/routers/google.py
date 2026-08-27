from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Request,
    Depends,
    HTTPException,
    status,
)

from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from authlib.integrations.starlette_client import OAuthError

from app.config import settings
from app.database import get_db

from app.models.user import User

from app.services.google_service import oauth
from app.services.token_service import create_refresh_token

from app.security.jwt import create_access_token


router = APIRouter(
    prefix="/auth/google",
    tags=["Google OAuth"]
)


# =========================================================
# GOOGLE LOGIN
# =========================================================

@router.get("/login")
async def google_login(request: Request):

    redirect_uri = settings.GOOGLE_REDIRECT_URI

    return await oauth.google.authorize_redirect(
        request,
        redirect_uri
    )


# =========================================================
# GOOGLE CALLBACK
# =========================================================

@router.get("/callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):

    try:

        # -------------------------------------------------
        # Exchange authorization code for Google tokens
        # -------------------------------------------------

        token = await oauth.google.authorize_access_token(
            request
        )

    except OAuthError as e:

        print("========================================")
        print("GOOGLE OAUTH ERROR")
        print("Error:", e)
        print("Error type:", type(e))
        print("Error code:", getattr(e, "error", None))
        print(
            "Error description:",
            getattr(e, "error_description", None)
        )
        print("========================================")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Google authentication failed",
                "error": getattr(e, "error", None),
                "description": getattr(
                    e,
                    "error_description",
                    None
                )
            }
        )

    # -----------------------------------------------------
    # Get Google user information
    # -----------------------------------------------------

    userinfo = token.get("userinfo")

    if not userinfo:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to retrieve Google user information"
        )

    # -----------------------------------------------------
    # Extract Google information
    # -----------------------------------------------------

    google_id = userinfo.get("sub")
    email = userinfo.get("email")
    full_name = userinfo.get("name")

    email_verified = userinfo.get(
        "email_verified",
        False
    )

    # -----------------------------------------------------
    # Validate Google response
    # -----------------------------------------------------

    if not google_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account ID was not provided"
        )

    if not email:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account email was not provided"
        )

    if not email_verified:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Google email is not verified"
        )

    # =====================================================
    # FIND USER BY GOOGLE ID
    # =====================================================

    user = (
        db.query(User)
        .filter(
            User.google_id == google_id
        )
        .first()
    )

    # =====================================================
    # IF GOOGLE USER DOES NOT EXIST
    # =====================================================

    if not user:

        # -------------------------------------------------
        # Check whether email already belongs to a user
        # -------------------------------------------------

        user = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        # -------------------------------------------------
        # Existing email account
        # -------------------------------------------------

        if user:

            # Link Google account to existing account
            user.google_id = google_id

            # Google has already verified the email
            user.email_verified = True

        # -------------------------------------------------
        # Completely new Google user
        # -------------------------------------------------

        else:

            user = User(
                full_name=full_name or email.split("@")[0],
                email=email,
                google_id=google_id,
                email_verified=True,
                phone_verified=False,
                is_active=True,
                role="user",
                password_hash=None,
            )

            db.add(user)

    # =====================================================
    # ACCOUNT STATUS CHECK
    # =====================================================

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # =====================================================
    # UPDATE LAST LOGIN
    # =====================================================

    user.last_login_at = datetime.now(
        timezone.utc
    )

    db.commit()

    db.refresh(user)

    # =====================================================
    # CREATE YOUR APPLICATION JWT
    # =====================================================

    access_token = create_access_token(
        user_id=str(user.id),
        role=user.role
    )

    # =====================================================
    # CREATE YOUR APPLICATION REFRESH TOKEN
    # =====================================================

    refresh_token = create_refresh_token(
        db=db,
        user_id=user.id
    )

    # =====================================================
    # REDIRECT TO FRONTEND
    # =====================================================

    return RedirectResponse(
        url=(
            f"{settings.FRONTEND_URL}"
            f"/google-callback"
            f"?access_token={access_token}"
            f"&refresh_token={refresh_token}"
        )
    )