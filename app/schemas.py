from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str

class ErrorResponse(BaseModel):
    detail: str
