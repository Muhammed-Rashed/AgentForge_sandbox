from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import bcrypt
import jwt

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/api/login")
def login(request: LoginRequest):
    expected_user = os.getenv("LOGIN_USERNAME")
    expected_hash = os.getenv("LOGIN_PASSWORD_HASH")
    if not expected_user or not expected_hash:
        raise HTTPException(status_code=500, detail="Login credentials not configured")
    if request.username != expected_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(request.password.encode(), expected_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    secret = os.getenv("JWT_SECRET", "secret")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    token = jwt.encode({"sub": request.username}, secret, algorithm=algorithm)
    return {"access_token": token, "token_type": "bearer"}
