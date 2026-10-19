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

@router.post("/login")
def login(request: LoginRequest):
    expected_user = os.getenv("APP_USERNAME")
    password_hash = os.getenv("APP_PASSWORD_HASH")
    jwt_secret = os.getenv("JWT_SECRET")
    if not all([expected_user, password_hash, jwt_secret]):
        raise HTTPException(status_code=500, detail="Server configuration error")
    if request.username != expected_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(request.password.encode(), password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {
        "sub": request.username,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
