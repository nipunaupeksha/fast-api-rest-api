from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from schemas.user import User, UserCreate, UserUpdate, UserPasswordUpdate
from schemas.pagination import PaginatedUserReponse
from handlers.user import (
    get_user_by_id,
    create_user,
    delete_user,
    get_users,
    update_user,
    update_user_password,
)
from api.deps import get_db, get_current_admin_user, get_current_user, get_user_by_email
from uuid import UUID
from typing import Optional

router = APIRouter()


# Get users with filter support
@router.get("/", response_model=PaginatedUserReponse, status_code=status.HTTP_200_OK)
def get_users_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    firstName: Optional[str] = Query(None),
    lastName: Optional[str] = Query(None),
    isAdmin: Optional[bool] = Query(None),
    email: Optional[str] = Query(None),
    username: Optional[str] = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    users, total = get_users(
        db=db,
        limit=limit,
        offset=offset,
        first_name=firstName,
        last_name=lastName,
        is_admin=isAdmin,
        email=email,
        username=username,
    )
    itemsPerPage = limit if limit < len(users) else len(users)
    return PaginatedUserReponse(
        totalResults=total, itemsPerPage=itemsPerPage, users=users
    )


# Create a new user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    return create_user(db=db, user=user)


# Delete a user
# Usually its 204 - No Content for DELETE requests, but here its better to get the delete user information
@router.delete("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def delete_user_endpoint(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return delete_user(db=db, user=user)


# Update a user
@router.patch("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def update_user_endpoint(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # If the current user is an admin user he can update any user's values
    # If not the user shold be updating the details of him/her self
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_user_info = get_user_by_email(db, current_user.email)
    if user.email != current_user.email and not current_user_info.is_admin:
        raise HTTPException(
            status_code=403, detail="User is forbidden to update the user"
        )

    updated_user = update_user(db=db, user_id=user_id, user_update=user_update)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user")

    return updated_user


# Get user by id
@router.get("/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
def get_user_endpoint(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # If the current user is an admin user he can update any user's values
    # If not the user shold be updating the details of him/her self
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_user_info = get_user_by_email(db, current_user.email)
    if user.email != current_user.email and not current_user_info.is_admin:
        raise HTTPException(
            status_code=403, detail="User is forbidden to view details of the user"
        )

    get_user = get_user_by_id(db=db, user_id=user_id)
    if not get_user:
        raise HTTPException(status_code=500, detail="Failed to update user")

    return get_user


# Change password
@router.patch(
    "/password/{user_id}", response_model=User, status_code=status.HTTP_200_OK
)
def update_user_password_endpoint(
    user_id: UUID,
    user_password_update: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # If the current user is an admin user he can update any user's values
    # If not the user shold be updating the details of him/her self
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    current_user_info = get_user_by_email(db, current_user.email)
    if user.email != current_user.email and not current_user_info.is_admin:
        raise HTTPException(
            status_code=403, detail="User is forbidden to update the user"
        )

    updated_user = update_user_password(
        db=db, user_id=user_id, password_data=user_password_update
    )
    if not updated_user:
        raise HTTPException(status_code=500, detail="Failed to update user")

    return updated_user
