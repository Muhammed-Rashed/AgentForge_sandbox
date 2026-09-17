from fastapi import FastAPI, HTTPException, status
from app.schemas import LoginRequest, TokenResponse
from app.auth import MOCK_USERS_DB, verify_password, create_access_token

app = FastAPI(title="Auth API", version="1.0.0")

@app.post("/api/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    identifier = payload.username or payload.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required"
        )
    
    user = None
    for u in MOCK_USERS_DB.values():
        if u["username"] == identifier or u["email"] == identifier:
            user = u
            break
            
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": str(user["id"]), "username": user["username"]})
    return TokenResponse(access_token=access_token, token_type="bearer")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Auth service is running"}
