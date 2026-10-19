from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import bcrypt
import jwt

router = APIRouter(prefix="/api", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):
    expected_user = os.getenv("ADMIN_USERNAME")
    expected_hash = os.getenv("ADMIN_PASSWORD_HASH")
    jwt_secret = os.getenv("JWT_SECRET", "secret")

    if not expected_user or not expected_hash:
        raise HTTPException(status_code=500, detail="Server not configured")

    if request.username != expected_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not bcrypt.checkpw(request.password.encode(), expected_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode({"sub": request.username}, jwt_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
