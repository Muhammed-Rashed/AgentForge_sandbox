from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api", tags=["auth"])

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def get_user_credentials() -> tuple[str, bytes]:
    """Retrieve expected username and bcrypt hashed password from env."""
    username = os.getenv("APP_USERNAME")
    password_hash = os.getenv("APP_PASSWORD_HASH")
    if not username or not password_hash:
        raise RuntimeError("User credentials not set in environment")
    return username, password_hash.encode()

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT secret not set in environment")
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm="HS256")

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    expected_user, expected_hash = get_user_credentials()
    if payload.username != expected_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not bcrypt.checkpw(payload.password.encode(), expected_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": payload.username})
    return TokenResponse(access_token=access_token)
