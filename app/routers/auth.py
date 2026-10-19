import os
import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
import jwt

# Simple in‑memory user store (email -> hashed password)
_user_db: dict[str, str] = {}

# Password hashing context
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration – secret must be provided via environment variable
_JWT_SECRET = os.getenv("JWT_SECRET")
if not _JWT_SECRET:
    raise RuntimeError("Environment variable JWT_SECRET is required for authentication")
_JWT_ALGORITHM = "HS256"
_JWT_EXP_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["auth"])

class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def _hash_password(password: str) -> str:
    return _pwd_context.hash(password)

def _verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)

def _create_access_token(email: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=_JWT_EXP_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, _JWT_SECRET, algorithm=_JWT_ALGORITHM)

def _decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

CurrentUser = Annotated[str, Depends(lambda authorization: _decode_token(_extract_token(authorization)))]

def _extract_token(authorization: str | None = Header(default=None, convert_underscores=False)) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    scheme, _, param = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme")
    return param

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(req: RegisterRequest):
    if req.email in _user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    _user_db[req.email] = _hash_password(req.password)
    return {"msg": "User registered successfully"}

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    hashed = _user_db.get(req.email)
    if not hashed or not _verify_password(req.password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = _create_access_token(req.email)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def read_me(current_user: CurrentUser):
    return {"email": current_user}
