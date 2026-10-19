import os
import datetime
from typing import Annotated

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()

# In‑memory user store: email -> hashed password
_USERS: dict[str, bytes] = {}

# Secret key for JWT – must be set in the environment
_JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
_JWT_ALGORITHM = "HS256"
_JWT_EXP_MINUTES = 30


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DashboardResponse(BaseModel):
    message: str
    email: EmailStr


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def _create_access_token(email: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=_JWT_EXP_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, _JWT_SECRET, algorithm=_JWT_ALGORITHM)


def _decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# Dependency to extract and verify JWT from the Authorization header
CurrentUser = Annotated[str, Depends(lambda authorization: _decode_token(_extract_token(authorization)))]


def _extract_token(authorization: str | None = Header(default=None, convert_underscores=False)) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    scheme, _, param = authorization.partition(" ")
    if scheme.lower() != "bearer" or not param:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")
    return param


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest) -> TokenResponse:
    if request.email in _USERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    _USERS[request.email] = _hash_password(request.password)
    token = _create_access_token(request.email)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest) -> TokenResponse:
    hashed = _USERS.get(request.email)
    if not hashed or not _verify_password(request.password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = _create_access_token(request.email)
    return TokenResponse(access_token=token)


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(current_user: CurrentUser) -> DashboardResponse:
    return DashboardResponse(message="Welcome to your dashboard!", email=current_user)
