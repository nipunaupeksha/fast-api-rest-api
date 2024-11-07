from sqlalchemy.orm import Session
from handlers.user import get_user_by_email, create_user
from schemas.user import UserCreate
from core.config import settings


def init_db(db: Session) -> None:
    # Default admin credentials
    default_admin_email = settings.ADMIN_EMAIL
    default_admin_password = settings.ADMIN_PASSWORD

    # Check if the default admin already exists
    admin_user = get_user_by_email(db, email=default_admin_email)
    if not admin_user:
        # Create the default admin user
        admin_user = UserCreate(
            email=default_admin_email,
            password=default_admin_password,
            username=settings.ADMIN_USERNAME,
            first_name="admin",
            last_name="admin",
            is_admin=True,
        )
        create_user(db=db, user=admin_user)
        print(f"Created default admin user with email: {default_admin_email}")
    else:
        print("Default admin user already exists")
