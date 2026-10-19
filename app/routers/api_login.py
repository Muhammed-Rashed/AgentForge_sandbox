import os
import datetime
from typing import Annotated

import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api", tags=["auth"])


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


def _get_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Environment variable {var_name} is not set")
    return value


@router.post("/login")
def login(request: LoginRequest) -> dict:
    # Retrieve expected credentials from environment variables
    expected_user = _get_env("LOGIN_USERNAME")
    expected_hash = _get_env("LOGIN_PASSWORD_HASH").encode()

    if request.username != expected_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not bcrypt.checkpw(request.password.encode(), expected_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    secret = _get_env("JWT_SECRET")
    payload = {
        "sub": request.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
