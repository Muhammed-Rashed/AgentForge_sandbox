from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, Token
from app.core.security import verify_password, create_access_token, get_password_hash

router = APIRouter(prefix="/api", tags=["auth"])

# Mock demo user for standard verification; in production this delegates to DB models
DEMO_USER = {
    "id": "1",
    "username": "admin",
    "email": "admin@example.com",
    "hashed_password": get_password_hash("password123")
}

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    identifier = credentials.username or credentials.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email must be provided"
        )

    is_valid_user = (identifier == DEMO_USER["username"] or identifier == DEMO_USER["email"])
    if not is_valid_user or not verify_password(credentials.password, DEMO_USER["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": DEMO_USER["username"], "user_id": DEMO_USER["id"]}
    )
    return Token(access_token=access_token, token_type="bearer")
