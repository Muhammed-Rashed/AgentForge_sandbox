import os
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Header, status
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()

# In‑memory user store: email -> hashed password (bytes)
_USERS: dict[str, bytes] = {}

# Environment variable for JWT secret (must be set in production)
_JWT_SECRET = os.getenv("JWT_SECRET", "change-me-secret")
_JWT_ALGORITHM = "HS256"
_JWT_EXPIRATION_HOURS = 1


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    email: EmailStr


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _verify_password(plain_password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed)


def _create_access_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=_JWT_EXPIRATION_HOURS)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)


def _decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])
        return payload.get("sub") or ""
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


CurrentUser = Annotated[str, Depends(lambda authorization: _decode_token(
    authorization.split(" ")[1] if authorization and authorization.startswith("Bearer ") else ""
))]


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest):
    if request.email in _USERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    _USERS[request.email] = _hash_password(request.password)
    return UserResponse(email=request.email)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    hashed = _USERS.get(request.email)
    if not hashed or not _verify_password(request.password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = _create_access_token(request.email)
    return TokenResponse(access_token=token)


@router.get("/dashboard")
def dashboard(current_user: CurrentUser):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return {"message": f"Welcome, {current_user}!", "email": current_user}
