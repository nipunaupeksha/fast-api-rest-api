from db.session import SessionLocal
from typing import Generator
from core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from handlers.user import get_user_by_email
from models.user import User
from handlers.token import check_token_invalid
from datetime import datetime, timezone

# OAuth2PasswordBearer instnace for dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_STR}/auth/sign-in")


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        is_invalid = check_token_invalid(db, token)
        if is_invalid:
            raise unauthorized_exception
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise unauthorized_exception
        exp: int = payload.get("exp")
        exp = datetime.fromtimestamp(exp, tz=timezone.utc)
        print(f"exp: {exp}, date: {datetime.utcnow()}")
        if exp < datetime.utcnow().replace(tzinfo=timezone.utc):
            raise unauthorized_exception
    except JWTError:
        raise unauthorized_exception

    # Fetch the user from the database
    user = get_user_by_email(db, email=email)
    if user is None:
        raise unauthorized_exception
    return user


# Get the current admin user details
def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges are required",
        )
    return current_user
