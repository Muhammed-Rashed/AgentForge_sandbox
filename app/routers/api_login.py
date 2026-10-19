from fastapi import APIRouter, HTTPException
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

def get_secret_key() -> str:
    key = os.getenv("JWT_SECRET_KEY")
    if not key:
        raise RuntimeError("JWT_SECRET_KEY environment variable not set")
    return key

def get_user_hashed_password(username: str) -> bytes | None:
    # Expect env var USER_{USERNAME}_HASH containing bcrypt hash
    env_name = f"USER_{username.upper()}_HASH"
    hash_str = os.getenv(env_name)
    return hash_str.encode() if hash_str else None

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    hashed = get_user_hashed_password(request.username)
    if not hashed or not bcrypt.checkpw(request.password.encode(), hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    secret = get_secret_key()
    expire = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": request.username, "exp": expire}
    token = jwt.encode(payload, secret, algorithm="HS256")
    return {"access_token": token}
