from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserPasswordUpdate
from core.security import hash_password, verify_password
from sqlalchemy.dialects.postgresql import UUID
from typing import List, Tuple, Optional
from fastapi import HTTPException, status


# Get users
def get_users(
    db: Session,
    limit: int = 10,
    offset: int = 0,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    is_admin: Optional[bool] = None,
    email: Optional[str] = None,
    username: Optional[str] = None,
) -> Tuple[List[User], int]:
    query = db.query(User)

    # Check filters
    if first_name is not None:
        query = query.filter(User.first_name.ilike(f"%{first_name}%"))
    if last_name is not None:
        query = query.filter(User.last_name.ilike(f"%{last_name}%"))
    if is_admin is not None:
        query = query.filter(User.is_admin == is_admin)
    if email is not None:
        query = query.filter(User.email == email)
    if username is not None:
        query = query.filter(User.username == username)

    # Get total count
    total = query.count()

    users = query.offset(offset).limit(limit).all()
    return users, total


# Filter a user by id
def get_user_by_id(db: Session, user_id: UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()


# Filter a user by username
def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()


# Filter a user by email
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


# Create a new user
def create_user(db: Session, user: UserCreate) -> User:
    # check for email duplication
    user_with_email = get_user_by_email(db=db, email=user.email)
    if user_with_email is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )
    # check for username duplication
    user_with_username = get_user_by_username(db=db, username=user.username)
    if user_with_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this username already exists.",
        )

    # proceed creating the user otherwise
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        is_admin=user.is_admin,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Authenticate a user using email + password
def authenticate_user_via_email(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email=email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


# If needed implement
# Authenticate a user using username + password
def authenticate_user_via_username(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username=username)
    if user and verify_password(password, user.hashed_password):
        return user
    return None


# Delete user
def delete_user(db: Session, user: User) -> User:
    db.delete(user)
    db.commit()
    return user


# Update user claims
def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
    # retrieve the user by ID
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    if user_update.first_name is not None:
        db_user.first_name = user_update.first_name
    if user_update.last_name is not None:
        db_user.last_name = user_update.last_name
    if user_update.is_admin is not None:
        db_user.is_admin = user_update.is_admin

    db.commit()
    db.refresh(db_user)
    return db_user

# Update user password
def update_user_password(
    db: Session, user_id: UUID, password_data: UserPasswordUpdate
) -> User:
    # Retrieve the user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify the old password
    if not verify_password(password_data.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )

    # Hash the new password and update it in the database
    user.hashed_password = hash_password(password_data.new_password)
    db.commit()
    db.refresh(user)
    return user
