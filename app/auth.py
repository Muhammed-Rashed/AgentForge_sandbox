from datetime import datetime, timedelta
from typing import Optional
from jose import jwt

SECRET_KEY = "secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

DEMO_USERS = {
    "admin": "admin123",
    "user@example.com": "password123",
    "user": "password123"
}

def verify_credentials(username: str, password: str) -> bool:
    return DEMO_USERS.get(username) == password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
