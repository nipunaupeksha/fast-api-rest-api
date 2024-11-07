from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.security import create_access_token
from schemas.token import Token
from schemas.user import User, UserCreate
from schemas.message import Message
from handlers.user import (
    create_user,
    authenticate_user_via_username,
)
from handlers.token import revoke_token
from api.deps import get_db, get_current_user, oauth2_scheme

router = APIRouter()


# User sign-in and get access token via password grant type
@router.post("/sign-in", response_model=Token)
def sign_in_endpoint(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user_via_username(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(db, data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# User sign-up
@router.post("/sign-up", response_model=User, status_code=status.HTTP_201_CREATED)
def sign_up_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user=user)
    return db_user


# User sign-out
@router.post("/sign-out", response_model=Message)
def sign_out_endpoint(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    token=Depends(oauth2_scheme),
):
    revoke_token(db, token)
    return {"message": f"{current_user.email} is logged out"}
