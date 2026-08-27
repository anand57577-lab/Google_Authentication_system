from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    SMTP_HOST : str

    SMTP_PORT: int = 465

    SMTP_USERNAME: str

    SMTP_PASSWORD: str

    SMTP_FROM_EMAIL: str

    SMTP_FROM_NAME: str = "Authentication System"

    FRONTEND_URL: str
    BACKEND_URL: str
    
        # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # Session security
    SESSION_SECRET_KEY: str

    EMAIL_VERIFICATION_EXPIRE_MINUTES: int = 30
    
    PASSWORD_RESET_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()