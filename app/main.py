from fastapi import FastAPI, HTTPException, status
from app.schemas import LoginRequest, TokenResponse
from app.auth import create_access_token

app = FastAPI(title="Auth API")

MOCK_USER = {"username": "admin", "password": "password123"}

@app.post("/api/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    if credentials.username != MOCK_USER["username"] or credentials.password != MOCK_USER["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": credentials.username})
    return TokenResponse(access_token=access_token, token_type="bearer")
