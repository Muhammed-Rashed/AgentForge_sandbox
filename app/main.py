from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, login, api_login
from pydantic import BaseModel
import os
import bcrypt
import jwt

app = FastAPI(title="Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(login.router)
app.include_router(api_login.router)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/api/login")
def login(request: LoginRequest):
    expected_user = os.getenv("LOGIN_USERNAME")
    expected_hash = os.getenv("LOGIN_PASSWORD_HASH")
    if not expected_user or not expected_hash:
        raise HTTPException(status_code=500, detail="Login credentials not configured")
    if request.username != expected_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not bcrypt.checkpw(request.password.encode(), expected_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    secret = os.getenv("JWT_SECRET", "secret")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")
    token = jwt.encode({"sub": request.username}, secret, algorithm=algorithm)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/")
def read_root():
    return {"message": "API status: OK"}
