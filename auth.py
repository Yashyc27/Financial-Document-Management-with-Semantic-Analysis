from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Role Definitions 
ROLES = {
    "Admin": ["full_access"],
    "Analyst": ["upload_doc", "edit_doc"],
    "Auditor": ["review_doc"],
    "Client": ["view_doc"]
}

def verify_role(required_permission: str, user_role: str):
    if required_permission not in ROLES.get(user_role, []):
        raise HTTPException(status_code=403, detail="Insufficient permissions")