from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()

# ponytail: in-memory user store for demonstration/testing
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("password123"),
    }
}

class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/api/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    identifier = credentials.username or credentials.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )

    user = None
    for u in FAKE_USERS_DB.values():
        if u["username"] == identifier or u["email"] == identifier:
            user = u
            break

    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user["username"], "email": user["email"]}
    )
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/api/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: RegisterRequest):
    if user_in.username in FAKE_USERS_DB or user_in.email in FAKE_USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    user_data = {
        "username": user_in.username,
        "email": user_in.email,
        "hashed_password": get_password_hash(user_in.password),
    }
    FAKE_USERS_DB[user_in.username] = user_data
    return {"message": "User registered successfully"}
