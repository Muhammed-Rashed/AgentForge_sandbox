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


@router.post("/login")
def login(data: LoginRequest):
    env_user = os.getenv("APP_USERNAME")
    env_hash = os.getenv("APP_PASSWORD_HASH")
    if not env_user or not env_hash:
        raise HTTPException(status_code=500, detail="Server not configured")
    if data.username != env_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not bcrypt.checkpw(data.password.encode(), env_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="JWT secret not set")
    payload = {
        "sub": data.username,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
