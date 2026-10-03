from typing import Dict, Optional
from app.core.config import settings
from app.core.security import get_password_hash

# ponytail: O(n) in-memory lookup dict, sufficient for lightweight backend auth
USERS_DB: Dict[str, dict] = {}

def init_db():
    if not USERS_DB:
        hashed = get_password_hash(settings.DEFAULT_USER_PASSWORD)
        user = {
            "id": "1",
            "username": settings.DEFAULT_USER_USERNAME,
            "email": settings.DEFAULT_USER_EMAIL,
            "hashed_password": hashed,
            "is_active": True,
        }
        USERS_DB[settings.DEFAULT_USER_USERNAME.lower()] = user
        USERS_DB[settings.DEFAULT_USER_EMAIL.lower()] = user

def get_user_by_identifier(identifier: str) -> Optional[dict]:
    init_db()
    return USERS_DB.get(identifier.lower())
