from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Auth API")

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

@app.post("/api/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    if not request.username or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required."
        )
    
    if request.password == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    return LoginResponse(
        access_token=f"mock-token-{request.username}",
        token_type="bearer",
        user={
            "username": request.username,
            "role": "user"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
