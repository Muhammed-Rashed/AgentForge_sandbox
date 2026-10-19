from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
import os
import bcrypt
import jwt

router = APIRouter(prefix="/api", tags=["auth"])


class LoginRequest(BaseModel):
    username: str = Field(..., description="The user's username")
    password: str = Field(..., description="The user's password")


@router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest):
    """Authenticate a user and return a JWT token.

    The expected environment variables are:
    - USERNAME: the allowed username
    - PASSWORD_HASH: bcrypt hash of the allowed password
    - JWT_SECRET: secret key for signing JWT tokens
    """
    expected_username = os.getenv("USERNAME")
    password_hash = os.getenv("PASSWORD_HASH")
    jwt_secret = os.getenv("JWT_SECRET")

    if not expected_username or not password_hash or not jwt_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication configuration is incomplete.",
        )

    if request.username != expected_username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not bcrypt.checkpw(request.password.encode(), password_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = jwt.encode({"sub": request.username}, jwt_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
