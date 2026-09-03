from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers import auth, google

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.config import settings


app = FastAPI(
    title="Authentication API",
    description="Authentication system using FastAPI and PostgreSQL",
    version="1.0.0"
)



app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://google-authentication-system.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(google.router)

@app.get("/")
def root():
    return {
        "message": "Authentication API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/health/db")
def database_health_check():

    try:
        with engine.connect() as connection:

            connection.execute(
                text("SELECT 1")
            )

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
