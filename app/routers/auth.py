from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, TokenResponse
from app.auth import DEMO_USERS, verify_password, create_access_token

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    user = DEMO_USERS.get(payload.username)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(user["id"]), "username": user["username"]}
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    )
