import os
import datetime
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext

# In‑memory user store (email -> hashed password)
_USERS: dict[str, str] = {}

# Password hashing context
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings from environment
_JWT_SECRET = os.getenv("JWT_SECRET_KEY", "change-me")
_JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
_JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def _hash_password(password: str) -> str:
    return _pwd_context.hash(password)

def _verify_password(plain: str, hashed: str) -> bool:
    return _pwd_context.verify(plain, hashed)

def _create_access_token(email: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=_JWT_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, _JWT_SECRET, algorithm=_JWT_ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if email not in _USERS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return email

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    if user.email in _USERS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    _USERS[user.email] = _hash_password(user.password)
    return {"msg": "User created"}

@router.post("/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    email = form_data.username
    password = form_data.password
    hashed = _USERS.get(email)
    if not hashed or not _verify_password(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = _create_access_token(email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def read_me(current_user: Annotated[str, Depends(get_current_user)]):
    return {"email": current_user}
