import os
import time
from typing import Annotated

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel

router = APIRouter()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 86400


def get_secret_key() -> str:
    return os.getenv("JWT_SECRET", "dev-secret-key-change-in-production")


def get_admin_username() -> str:
    return os.getenv("AUTH_USERNAME", "admin")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


class UserResponse(BaseModel):
    username: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def create_access_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS,
    }
    return jwt.encode(payload, get_secret_key(), algorithm=ALGORITHM)


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    expected_username = get_admin_username()

    if credentials.username != expected_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    env_password = os.getenv("AUTH_PASSWORD")
    env_hash = os.getenv("AUTH_PASSWORD_HASH")

    if env_hash:
        valid = verify_password(credentials.password, env_hash)
    elif env_password:
        valid = (credentials.password == env_password)
    else:
        valid = (credentials.password == "admin123")

    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(credentials.username)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        username=credentials.username,
    )


def get_current_user(authorization: Annotated[str | None, Header()] = None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid token",
        )
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, get_secret_key(), algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        return username
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


CurrentUserDep = Annotated[str, Depends(get_current_user)]


@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUserDep) -> UserResponse:
    return UserResponse(username=current_user)
