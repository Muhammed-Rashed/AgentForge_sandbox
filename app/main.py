from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, login, api_login, login_endpoint, login_api, login_post, login_post_new
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
app.include_router(login_endpoint.router)
app.include_router(login_api.router)
app.include_router(login_post.router)
app.include_router(login_post_new.router)


class LoginRequest(BaseModel):
    username: str
    password: str


# login endpoint moved to router


@app.get("/")
def read_root():
    return {"message": "API status: OK"}


@app.post("/api/login")
def login(request: LoginRequest):
    if not request.username or not request.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Server misconfiguration")
    # Retrieve stored bcrypt hash for the user; for simplicity, use a single env var
    stored_hash = os.getenv("USER_PASSWORD_HASH")
    if not stored_hash:
        raise HTTPException(status_code=500, detail="Server misconfiguration")
    if not bcrypt.checkpw(request.password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": request.username}, secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
