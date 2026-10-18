import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.security import (
    DashboardResponse,
    TokenResponse,
    UserLogin,
    UserRegister,
    UserResponse,
    create_access_token,
    get_current_user,
    hash_password,
    users_db,
    verify_password,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def register(user_data: UserRegister) -> UserResponse:
    email_key = user_data.email.lower()
    if email_key in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user_id = str(uuid.uuid4())
    users_db[email_key] = {
        "id": user_id,
        "email": user_data.email,
        "password_hash": hash_password(user_data.password),
    }
    return UserResponse(id=user_id, email=user_data.email)


@router.post("/login", response_model=TokenResponse)
@router.post("/auth/login", response_model=TokenResponse, include_in_schema=False)
def login(credentials: UserLogin) -> TokenResponse:
    email = credentials.login_email.lower()
    if not email or email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    user = users_db[email]
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token({"sub": user["email"], "email": user["email"]})
    user_resp = UserResponse(id=user["id"], email=user["email"])
    return TokenResponse(access_token=access_token, token_type="bearer", user=user_resp)


@router.get("/me", response_model=UserResponse)
@router.get("/auth/me", response_model=UserResponse, include_in_schema=False)
def get_me(current_user: Annotated[dict, Depends(get_current_user)]) -> UserResponse:
    return UserResponse(id=current_user["id"], email=current_user["email"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(current_user: Annotated[dict, Depends(get_current_user)]) -> DashboardResponse:
    user_resp = UserResponse(id=current_user["id"], email=current_user["email"])
    return DashboardResponse(
        message=f"Welcome back, {current_user['email']}!",
        email=current_user["email"],
        user=user_resp,
    )
