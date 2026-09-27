from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta

app = FastAPI(title="Auth API", version="1.0.0")

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

MOCK_USERS = [
    {
        "id": "1",
        "username": "admin",
        "email": "admin@example.com",
        "password": "password123"
    },
    {
        "id": "2",
        "username": "user",
        "email": "user@example.com",
        "password": "userpass"
    }
]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=60))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/login", response_model=TokenResponse)
def login(login_data: LoginRequest):
    if not login_data.username and not login_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )
    user = None
    for u in MOCK_USERS:
        if login_data.username and u["username"] == login_data.username:
            user = u
            break
        if login_data.email and u["email"] == login_data.email:
            user = u
            break
    if not user or user["password"] != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(data={"sub": user["id"], "username": user["username"]})
    return TokenResponse(access_token=access_token, token_type="bearer")

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
