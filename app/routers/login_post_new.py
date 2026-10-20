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
    # In a real application, retrieve the stored password hash from a database.
    # Here we use an environment variable per user for demonstration purposes.
    stored_hash = os.getenv(f"{request.username.upper()}_HASH")
    if not stored_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(request.password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Server misconfiguration")
    token = jwt.encode({"sub": request.username}, secret, algorithm="HS256")
    return {"access_token": token}
