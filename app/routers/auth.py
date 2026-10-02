from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/api", tags=["Authentication"])

MOCK_USERS = {
    "admin": "admin123",
    "user@example.com": "password123"
}

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    stored_password = MOCK_USERS.get(credentials.username)
    if not stored_password or stored_password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(access_token=f"fake-jwt-token-for-{credentials.username}", token_type="bearer")
