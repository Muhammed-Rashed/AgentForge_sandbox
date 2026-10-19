from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Annotated
import os
import bcrypt
import jwt

router = APIRouter(prefix="/api", tags=["auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest) -> dict:
    # Retrieve the bcrypt hash for the user from environment variables.
    # Expected env var format: USER_<USERNAME>_HASH (e.g., USER_ALICE_HASH)
    env_var = f"USER_{request.username.upper()}_HASH"
    stored_hash = os.getenv(env_var)
    if not stored_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(request.password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    secret_key = os.getenv("JWT_SECRET_KEY")
    if not secret_key:
        raise HTTPException(status_code=500, detail="Server configuration error")
    token = jwt.encode({"sub": request.username}, secret_key, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
