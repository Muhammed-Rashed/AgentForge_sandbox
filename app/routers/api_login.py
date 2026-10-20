from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import os
import bcrypt
import jwt

router = APIRouter(prefix="/api", tags=["auth"])

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

@router.post("/login")
def login(request: LoginRequest):
    expected_user = os.getenv("APP_USERNAME")
    password_hash = os.getenv("APP_PASSWORD_HASH")
    if not expected_user or not password_hash:
        raise HTTPException(status_code=500, detail="Server configuration error")
    if request.username != expected_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(request.password.encode(), password_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Server configuration error")
    token = jwt.encode({"sub": request.username}, secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
