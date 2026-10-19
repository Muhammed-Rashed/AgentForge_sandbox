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

def get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET environment variable not set")
    return secret

# Simple in‑memory user store with bcrypt‑hashed passwords.
# Replace with a real database in production.
_user_passwords = {
    "alice": bcrypt.hashpw(b"alicepassword", bcrypt.gensalt()),
    "bob": bcrypt.hashpw(b"bobpassword", bcrypt.gensalt()),
}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    stored_hash = _user_passwords.get(data.username)
    if not stored_hash or not bcrypt.checkpw(data.password.encode(), stored_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": data.username,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, get_jwt_secret(), algorithm="HS256")
    return TokenResponse(access_token=token)
