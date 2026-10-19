from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import os
import bcrypt
import jwt
from datetime import datetime, timedelta

router = APIRouter(prefix="/api", tags=["auth"])

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def _verify_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password)

def _create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise RuntimeError("JWT_SECRET_KEY environment variable not set")
    return jwt.encode(to_encode, secret_key, algorithm="HS256")

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    # Expected credentials from environment variables
    expected_username = os.getenv("APP_USERNAME")
    expected_password_hash = os.getenv("APP_PASSWORD_HASH")
    if not expected_username or not expected_password_hash:
        raise RuntimeError("Authentication environment variables not set")

    if request.username != expected_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not _verify_password(request.password, expected_password_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = _create_access_token({"sub": request.username})
    return TokenResponse(access_token=access_token)
