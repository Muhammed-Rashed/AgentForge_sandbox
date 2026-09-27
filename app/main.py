from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Auth API", version="1.0.0")

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

DEMO_USERS = {
    "admin": "secret123",
    "user@example.com": "password123"
}

@app.post("/api/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    stored_password = DEMO_USERS.get(credentials.username)
    if not stored_password or stored_password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    mock_token = f"fake-jwt-token-for-{credentials.username}"
    return TokenResponse(
        access_token=mock_token,
        token_type="bearer",
        username=credentials.username
    )

@app.get("/health")
async def health_check():
    return {"status": "ok"}
