import os
from datetime import datetime, timedelta, timezone
from typing import Any
import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

load_dotenv()

router = APIRouter(tags=["auth"])

SECRET_KEY = os.getenv("JWT_SECRET") or os.getenv("SECRET_KEY") or "default_jwt_secret_key_change_in_production"
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

DEFAULT_HASH = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

AUTH_USER = os.getenv("AUTH_USER") or os.getenv("ADMIN_USERNAME") or "admin"
AUTH_EMAIL = os.getenv("AUTH_EMAIL") or os.getenv("ADMIN_EMAIL") or "admin@example.com"
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD") or os.getenv("ADMIN_PASSWORD")

if AUTH_PASSWORD:
    AUTH_PASSWORD_HASH = bcrypt.hashpw(AUTH_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
else:
    AUTH_PASSWORD_HASH = DEFAULT_HASH


class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict[str, Any] | None = None


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/api/login", response_model=TokenResponse)
@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    identifier = request.username or request.email
    if not identifier or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email and password are required",
        )

    is_user_match = (
        (request.username and request.username.lower() == AUTH_USER.lower())
        or (request.email and request.email.lower() == AUTH_EMAIL.lower())
        or (identifier.lower() in (AUTH_USER.lower(), AUTH_EMAIL.lower()))
    )

    is_password_correct = bcrypt.checkpw(
        request.password.encode("utf-8"),
        AUTH_PASSWORD_HASH.encode("utf-8"),
    )

    if not is_user_match or not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": identifier, "user": AUTH_USER})
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user={"username": AUTH_USER, "email": AUTH_EMAIL},
    )
