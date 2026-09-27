from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, TokenResponse
from app.auth import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/api", tags=["auth"])

# Mock database for authentication
USERS_DB = {
    "admin": {
        "id": 1,
        "username": "admin",
        "hashed_password": get_password_hash("password123"),
        "role": "admin"
    },
    "user@example.com": {
        "id": 2,
        "username": "user@example.com",
        "hashed_password": get_password_hash("password123"),
        "role": "user"
    }
}

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    user = USERS_DB.get(credentials.username)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user["username"], "user_id": user["id"], "role": user["role"]}
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user["id"],
        username=user["username"]
    )
