import os
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_secret = os.getenv("JWT_SECRET", "change-me")  # fallback for development only

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Simple in‑memory user store: email -> hashed password
_user_db: dict[str, str] = {}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(hours=1)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, jwt_secret, algorithm="HS256")

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=["HS256"])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

security = HTTPBearer()

def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    return decode_token(credentials.credentials)

@router.post("/register", response_model=TokenResponse)
def register(data: RegisterRequest):
    if data.email in _user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    _user_db[data.email] = hash_password(data.password)
    token = create_access_token(data.email)
    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    hashed = _user_db.get(data.email)
    if not hashed or not verify_password(data.password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(data.email)
    return {"access_token": token}

@router.get("/dashboard")
def dashboard(user: Annotated[str, Depends(get_current_user)]):
    return {"message": f"Welcome, {user}!", "email": user}
