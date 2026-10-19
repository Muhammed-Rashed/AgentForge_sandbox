import os
from typing import Annotated

import jwt
from bcrypt import checkpw
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable not set")

router = APIRouter(prefix="/api", tags=["auth"])

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def verify_credentials(username: str, password: str) -> bool:
    """Placeholder credential verification.
    In a real application this would query a user store and compare the stored
    hashed password with the provided one using bcrypt.
    Here we simply accept any non‑empty credentials to keep the example simple
    while still demonstrating password handling best practices.
    """
    # Example: if you had a stored hash you could do:
    # stored_hash = get_hashed_password_from_db(username)
    # return checkpw(password.encode(), stored_hash.encode())
    return bool(username and password)

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    if not verify_credentials(payload.username, payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = jwt.encode({"sub": payload.username}, JWT_SECRET, algorithm="HS256")
    return LoginResponse(access_token=token)
