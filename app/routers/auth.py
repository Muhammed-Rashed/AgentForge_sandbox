from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, TokenResponse
from app.auth import MOCK_USERS_DB, verify_password, create_access_token

router = APIRouter(prefix="/api", tags=["Auth"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    username_or_email = request.username or request.email
    if not username_or_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email must be provided"
        )

    user = None
    for u in MOCK_USERS_DB.values():
        if u["username"] == username_or_email or u["email"] == username_or_email:
            user = u
            break

    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["user_id"], "username": user["username"]})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user["user_id"],
        username=user["username"]
    )
