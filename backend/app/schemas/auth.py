from pydantic import BaseModel, EmailStr, Field, model_validator
from uuid import UUID
from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    @model_validator(mode="after")
    def validate_registration(self):

        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")

        password = self.password

        if not any(char.isupper() for char in password):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not any(char.islower() for char in password):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not any(char.isdigit() for char in password):
            raise ValueError(
                "Password must contain at least one number"
            )

        if not any(
            char in "!@#$%^&*()_+-=[]{}|;:,.<>?"
            for char in password
        ):
            raise ValueError(
                "Password must contain at least one special character"
            )

        return self


class LoginRequest(BaseModel):
    """
    Data required for email/password login.
    """

    email: EmailStr

    password: str = Field(
        ...,
        min_length=1,
        max_length=128
    )

class TokenResponse(BaseModel):
    access_token:str
    refresh_token: str
    token_type:str = "bearer"



class UserResponse(BaseModel):
    """
    Safe user information returned by the API.

    Never return password_hash.
    """

    id: UUID
    full_name: str
    email: str | None
    phone_number: str | None
    email_verified: bool
    phone_verified: bool
    is_active: bool
    role: str

class RefreshTokenRequest(BaseModel):

    refresh_token: str


class EmailVerificationRequest(BaseModel):

    token: str

class ResendVerificationRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str