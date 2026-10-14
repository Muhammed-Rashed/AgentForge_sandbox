import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key_change_in_production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

DEFAULT_USERNAME = os.getenv("AUTH_USERNAME", os.getenv("DEFAULT_USERNAME", "admin"))
DEFAULT_EMAIL = os.getenv("AUTH_EMAIL", "admin@example.com")
_ENV_PASSWORD = os.getenv("AUTH_PASSWORD", os.getenv("ADMIN_PASSWORD", "admin123"))
_ENV_PASSWORD_HASH = os.getenv("AUTH_PASSWORD_HASH", "")

if _ENV_PASSWORD_HASH:
    DEFAULT_PASSWORD_HASH = _ENV_PASSWORD_HASH
else:
    DEFAULT_PASSWORD_HASH = bcrypt.hashpw(_ENV_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: Optional[str] = None


@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    identifier = request.username or request.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required",
        )

    is_valid_user = (
        (request.username and request.username.lower() == DEFAULT_USERNAME.lower())
        or (request.email and request.email.lower() == DEFAULT_EMAIL.lower())
        or (identifier.lower() == DEFAULT_USERNAME.lower())
        or (identifier.lower() == DEFAULT_EMAIL.lower())
    )

    if not is_valid_user or not verify_password(request.password, DEFAULT_PASSWORD_HASH):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {"sub": DEFAULT_USERNAME, "email": DEFAULT_EMAIL}
    access_token = create_access_token(data=token_data)

    return Token(
        access_token=access_token,
        token_type="bearer",
        username=DEFAULT_USERNAME,
    )
