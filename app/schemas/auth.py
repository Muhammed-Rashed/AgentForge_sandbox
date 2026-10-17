from typing import Optional
from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str


class UserResponse(BaseModel):
    username: str
    email: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[UserResponse] = None
