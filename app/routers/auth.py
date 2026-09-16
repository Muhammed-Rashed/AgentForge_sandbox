from fastapi import APIRouter, HTTPException, status
from app.schemas import LoginRequest, TokenResponse, UserResponse
from app.auth import authenticate_user, create_access_token

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    identifier = credentials.username or credentials.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )
    
    user = authenticate_user(identifier, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user["id"]), "username": user["username"]})
    user_response = UserResponse(id=user["id"], username=user["username"], email=user["email"])
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )
