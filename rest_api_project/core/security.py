from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from core.config import settings
from sqlalchemy.orm import Session
from handlers.token import save_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash the plain password using bcrypt algorithm
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Verify the provided plain password and the hashed password obtained from the db
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Create an access token
def create_access_token(db: Session, data: dict, expires_detla: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_detla
        if expires_detla
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    save_token(db, token, expire)
    return token
