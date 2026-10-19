import os
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(request: LoginRequest):
    # Load expected credentials from environment
    expected_user = os.getenv("APP_USERNAME")
    expected_hash = os.getenv("APP_PASSWORD_HASH")
    jwt_secret = os.getenv("APP_JWT_SECRET")
    jwt_algo = os.getenv("APP_JWT_ALGORITHM", "HS256")

    if not expected_user or not expected_hash or not jwt_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication configuration is missing",
        )

    if request.username != expected_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not bcrypt.checkpw(request.password.encode(), expected_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = jwt.encode({"sub": request.username}, jwt_secret, algorithm=jwt_algo)
    return {"access_token": token, "token_type": "bearer"}
