"""
Authentication system for admin dashboard
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "coaching-site-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Superuser credentials (in production, store in database)
SUPERUSER_USERNAME = "peterstoyanov"
SUPERUSER_PASSWORD_HASH = "$2b$12$C8M1rgwWl/6bAqLn1F0geupNPeFnMB7iD9KOKX/kA2pOkjs6vRYtq"  # CoachingMaster2024!

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    is_admin: bool = False

def verify_password(plain_password, hashed_password):
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Hash a password"""
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    """Authenticate a user"""
    if username != SUPERUSER_USERNAME:
        return False
    
    if not verify_password(password, SUPERUSER_PASSWORD_HASH):
        return False
    
    return User(username=username, is_admin=True)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    if token_data.username != SUPERUSER_USERNAME:
        raise credentials_exception
    
    return User(username=token_data.username, is_admin=True)

async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    """Ensure the current user is an admin"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

def generate_superuser_password():
    """Generate a new superuser password hash (for setup)"""
    password = "CoachingMaster2024!"
    return get_password_hash(password)

if __name__ == "__main__":
    # Generate password hash for superuser
    print("Superuser Password Hash:")
    print(generate_superuser_password())
    print(f"Username: {SUPERUSER_USERNAME}")
    print("Password: CoachingMaster2024!")