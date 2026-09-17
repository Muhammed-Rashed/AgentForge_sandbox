from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Auth Service API")

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@app.post("/api/login", response_model=TokenResponse)
def login(credentials: LoginRequest):
    if not credentials.username or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required"
        )
    if credentials.username == "admin" and credentials.password == "admin123":
        return TokenResponse(access_token="sample_token_admin_12345")
    return TokenResponse(access_token=f"sample_token_{credentials.username}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
