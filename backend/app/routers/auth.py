from fastapi import (APIRouter, Depends, HTTPException, status,)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.security.password import hash_password
from app.security.password_reset import hash_password_reset_token
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
    RefreshTokenRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

from app.models.password_reset import PasswordResetToken

from app.security.password_reset import (
    hash_password_reset_token,
)

from app.services.token_service import (
    create_refresh_token,
    get_refresh_token,
)
from app.services.auth_service import authenticate_user

from app.security.jwt import create_access_token

from app.schemas.auth import UserResponse

from app.security.dependencies import get_current_user

from app.services.token_service import (
    create_refresh_token,
)

from app.models.email_verification import (
    EmailVerificationToken,
)

from app.security.email_verification import (
    hash_email_verification_token,
)

from app.schemas.auth import (
    EmailVerificationRequest,
    ResendVerificationRequest,
)

from app.services.email_verification_service import (
    create_email_verification_token,
    resend_email_verification_token,
)

from app.services.email_service import (
    send_verification_email,
    send_password_reset_email
)

from app.services.password_reset_service import (
    create_password_reset_token,
)

from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    request: RegisterRequest,
    # background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    print("===================================")
    print("REGISTER ENDPOINT STARTED")
    print("Email:", request.email)
    print("===================================")

    # 1. Check whether email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    # 2. Hash the password
    hashed_password = hash_password(
        request.password
    )

    # 3. Create new user
    new_user = User(
        full_name=request.full_name,
        email=request.email,
        password_hash=hashed_password
    )

    # 4. Add user to database
    db.add(new_user)

    # 5. Commit transaction
    db.commit()

    # 6. Refresh object to get generated values
    db.refresh(new_user)

    verification_token = (
    create_email_verification_token(
        db=db,
        user_id=new_user.id,
       )    
    )

    print("About to send mail")

    await send_verification_email(
    new_user.email,
    new_user.full_name,
    verification_token,
)

    print("EMAIL BACKGROUND TASK ADDED")

    return {
        "message": "Account created successfully"
                    "Please check your email to verify your account.",
                    
        "user_id": str(new_user.id)
    }

@router.post(
    "/login",
    response_model=TokenResponse
)
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email before logging in",
        )

    # Update last login time
    user.last_login_at = datetime.now(
        timezone.utc
    )

    db.commit()

    # Generate JWT
    access_token = create_access_token(
        user_id=str(user.id),
        role=user.role
    )

    refresh_token = create_refresh_token(
    db=db,
    user_id=user.id,
)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):

    return current_user


@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_access_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    stored_token = get_refresh_token(
        db=db,
        raw_token=request.refresh_token,
    )

    # Token doesn't exist
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Token already revoked
    if stored_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked",
        )

    # Token expired
    if stored_token.expires_at <= datetime.now(
        timezone.utc
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
        )

    # Get user
    user = (
        db.query(User)
        .filter(
            User.id == stored_token.user_id
        )
        .first()
    )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not available",
        )

    # Revoke old refresh token
    stored_token.revoked = True
    stored_token.revoked_at = datetime.now(
        timezone.utc
    )

    # Create new access token
    access_token = create_access_token(
        user_id=str(user.id),
        role=user.role,
    )

    # Create new refresh token
    new_refresh_token = create_refresh_token(
        db=db,
        user_id=user.id,
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post(
    "/logout"
)
def logout(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):

    stored_token = get_refresh_token(
        db=db,
        raw_token=request.refresh_token,
    )

    if not stored_token:
        return {
            "message": "Logged out successfully"
        }

    if not stored_token.revoked:

        stored_token.revoked = True

        stored_token.revoked_at = (
            datetime.now(timezone.utc)
        )

        db.commit()

    return {
        "message": "Logged out successfully"
    }

@router.post(
    "/verify-email"
)
def verify_email(
    request: EmailVerificationRequest,
    db: Session = Depends(get_db),
):

    token_hash = (
        hash_email_verification_token(
            request.token
        )
    )

    verification_token = (
        db.query(EmailVerificationToken)
        .filter(
            EmailVerificationToken.token_hash
            == token_hash
        )
        .first()
    )

    if not verification_token:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token",
        )

    if verification_token.used:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has already been used",
        )

    if (
        verification_token.expires_at
        <= datetime.now(timezone.utc)
    ):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired",
        )

    user = (
        db.query(User)
        .filter(
            User.id == verification_token.user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Mark email as verified
    user.email_verified = True

    # Mark token as used
    verification_token.used = True

    verification_token.used_at = (
        datetime.now(timezone.utc)
    )

    db.commit()

    return {
        "message": "Email verified successfully"
    }
    
@router.get("/verify-email")
def verify_email_from_link(
    token: str,
    db: Session = Depends(get_db),
):
    token_hash = hash_email_verification_token(token)

    verification_token = (
        db.query(EmailVerificationToken)
        .filter(
            EmailVerificationToken.token_hash == token_hash
        )
        .first()
    )

    if not verification_token:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/verify-email?status=invalid"
        )

    if verification_token.used:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/verify-email?status=already-used"
        )

    if (
        verification_token.expires_at
        <= datetime.now(timezone.utc)
    ):
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/verify-email?status=expired"
        )

    user = (
        db.query(User)
        .filter(
            User.id == verification_token.user_id
        )
        .first()
    )

    if not user:
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/verify-email?status=invalid"
        )

        # Mark email as verified
    user.email_verified = True

        # Mark token as used
    verification_token.used = True

    verification_token.used_at = (
        datetime.now(timezone.utc)
    )

    db.commit()

    return RedirectResponse(
        url=f"{settings.FRONTEND_URL}/verify-email?status=success"
    )   
        

@router.post("/resend-verification")
async def resend_verification_email(
    request: ResendVerificationRequest,
    db: Session = Depends(get_db),
):

    print("===================================")
    print("RESEND VERIFICATION ENDPOINT")
    print("Email:", request.email)
    print("===================================")

    # 1. Find user
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    # Don't reveal whether the account exists
    if not user:
        return {
            "message": (
                "If an account exists with this email, "
                "a verification email has been sent."
            )
        }

    # 2. If already verified, don't send another email
    if user.email_verified:
        return {
            "message": "This email address is already verified."
        }

    print("User found:", user.email)
    print("Generating new verification token...")

    # 3. Revoke/invalidate previous tokens
    verification_token = (
        resend_email_verification_token(
            db=db,
            user_id=user.id,
        )
    )

    print("New verification token generated")
    print("Sending verification email...")

    # 4. Send new email
    await send_verification_email(
        user.email,
        user.full_name,
        verification_token,
    )

    print("Verification email sent successfully")
    print("===================================")

    return {
        "message": (
            "A new verification email has been sent. "
            "Please check your inbox."
        )
    }

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    print("===================================")
    print("FORGOT PASSWORD ENDPOINT")
    print("Email:", request.email)
    print("===================================")

    # Find the user
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    # Always return the same response if the account
    # does not exist.
    if not user:
        print("No matching account found")
        return {
            "message": (
                "If an account exists with this email, "
                "a password reset email has been sent."
            )
        }

    # Password reset is only applicable to accounts
    # that actually have a password.
    if not user.password_hash:
        print("Account does not use password authentication")
        return {
            "message": (
                "If an account exists with this email, "
                "a password reset email has been sent."
            )
        }

    # Don't allow inactive accounts to reset passwords.
    if not user.is_active:
        print("Account is inactive")
        return {
            "message": (
                "If an account exists with this email, "
                "a password reset email has been sent."
            )
        }

    print("User found:", user.email)
    print("Generating password reset token...")

    # Generate and store HASHED token
    reset_token = create_password_reset_token(
        db=db,
        user_id=user.id,
    )

    print("Password reset token generated")
    print("Sending password reset email...")

    # Send raw token only through email
    await send_password_reset_email(
        recipient_email=user.email,
        full_name=user.full_name,
        reset_token=reset_token,
    )

    print("Password reset email sent successfully")
    print("===================================")

    return {
        "message": (
            "If an account exists with this email, "
            "a password reset email has been sent."
        )
    }

@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    print("===================================")
    print("RESET PASSWORD ENDPOINT")
    print("===================================")

    # --------------------------------------------------
    # 1. Check that passwords match
    # --------------------------------------------------

    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match",
        )

    # --------------------------------------------------
    # 2. Hash the token received from the user
    # --------------------------------------------------

    token_hash = hash_password_reset_token(
        request.token
    )

    print("Reset token received and hashed")

    # --------------------------------------------------
    # 3. Find the reset token
    # --------------------------------------------------

    reset_token = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash
        )
        .first()
    )

    if not reset_token:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token",
        )

    # --------------------------------------------------
    # 4. Check whether token was already used
    # --------------------------------------------------

    if reset_token.used:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token",
        )

    # --------------------------------------------------
    # 5. Check token expiry
    # --------------------------------------------------

    now = datetime.now(timezone.utc)

    if reset_token.expires_at <= now:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired password reset token",
        )

    # --------------------------------------------------
    # 6. Find the user
    # --------------------------------------------------

    user = (
        db.query(User)
        .filter(
            User.id == reset_token.user_id
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid password reset request",
        )

    # --------------------------------------------------
    # 7. Hash the new password using Argon2
    # --------------------------------------------------

    user.password_hash = hash_password(
        request.new_password
    )

    # --------------------------------------------------
    # 8. Mark this reset token as used
    # --------------------------------------------------

    reset_token.used = True
    reset_token.used_at = now

    # --------------------------------------------------
    # 9. Invalidate any other unused reset tokens
    # --------------------------------------------------

    other_tokens = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.used == False,
            PasswordResetToken.id != reset_token.id,
        )
        .all()
    )

    for token in other_tokens:
        token.used = True
        token.used_at = now

    # --------------------------------------------------
    # 10. Save everything
    # --------------------------------------------------

    db.commit()

    print("Password updated successfully")
    print("Reset token marked as used")
    print("===================================")

    return {
        "message": "Password reset successfully",
    }