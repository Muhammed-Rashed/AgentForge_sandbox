from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key-keep-it-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MOCK_USERS_DB = {
    "admin": {
        "user_id": "usr_01",
        "username": "admin",
        "email": "admin@example.com",
        "password_hash": pwd_context.hash("admin123"),
    },
    "user": {
        "user_id": "usr_02",
        "username": "user",
        "email": "user@example.com",
        "password_hash": pwd_context.hash("user123"),
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
