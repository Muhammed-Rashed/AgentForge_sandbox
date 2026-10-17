from fastapi import APIRouter, HTTPException, status
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/api", tags=["auth"])

# ponytail: in-memory user registry backed by environment variables for lightweight auth
_admin_hash = get_password_hash(settings.ADMIN_PASSWORD)
DEMO_USERS = {
    settings.ADMIN_USERNAME.lower(): {
        "username": settings.ADMIN_USERNAME,
        "email": settings.ADMIN_EMAIL,
        "password_hash": _admin_hash,
    }
}
if settings.ADMIN_EMAIL:
    DEMO_USERS[settings.ADMIN_EMAIL.lower()] = DEMO_USERS[settings.ADMIN_USERNAME.lower()]


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    identifier = (payload.username or payload.email or "").strip().lower()
    if not identifier or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email and password are required",
        )

    user = DEMO_USERS.get(identifier)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user["username"])
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            username=user["username"],
            email=user["email"],
        ),
    )
