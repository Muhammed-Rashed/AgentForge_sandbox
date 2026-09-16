from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import jwt

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DUMMY_USERS = {
    "user@example.com": {
        "email": "user@example.com",
        "username": "testuser",
        "password": "password123",
    },
    "admin@example.com": {
        "email": "admin@example.com",
        "username": "admin",
        "password": "adminpassword",
    }
}

app = FastAPI(title="Auth API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/api/login", response_model=TokenResponse)
def login(login_data: LoginRequest):
    user = None
    for u in DUMMY_USERS.values():
        if u["email"] == login_data.username or u["username"] == login_data.username:
            user = u
            break
    
    if not user or user["password"] != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "username": user["username"]},
        expires_delta=access_token_expires
    )
    return TokenResponse(access_token=access_token, token_type="bearer")

@app.get("/health")
def health_check():
    return {"status": "ok"}
