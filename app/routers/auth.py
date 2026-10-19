from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
import os
from datetime import datetime, timedelta
import bcrypt
import jwt

router = APIRouter()

# In‑memory user store (email -> user dict)
users: dict[str, dict] = {}

# JWT configuration – secret read from environment
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if email is None or email not in users:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return users[email]
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest):
    if req.email in users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    hashed = get_password_hash(req.password)
    users[req.email] = {"email": req.email, "hashed_password": hashed}
    access_token = create_access_token(data={"sub": req.email})
    return {"access_token": access_token}


@router.post("/login", response_model=TokenResponse)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token}


@router.get("/dashboard")
def dashboard(current_user: Annotated[dict, Depends(get_current_user)]):
    return {"message": f"Welcome, {current_user['email']}!"}
