from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, Token
from app.auth import create_access_token

router = APIRouter(prefix="/api", tags=["auth"])

DEMO_USERS = {
    "admin": "password123",
    "user@example.com": "password123"
}

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    username = credentials.username
    password = credentials.password
    
    if username not in DEMO_USERS or DEMO_USERS[username] != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": username})
    return Token(access_token=access_token, token_type="bearer")
