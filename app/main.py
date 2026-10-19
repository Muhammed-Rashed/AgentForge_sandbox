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


# login endpoint moved to router


@app.get("/")
def read_root():
    return {"message": "API status: OK"}
