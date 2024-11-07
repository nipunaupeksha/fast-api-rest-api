from fastapi import FastAPI
from api.endpoints import auth, users
from db.session import engine, SessionLocal
from db.base import Base
from core.config import settings
from db.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware

# Create the entry point
app = FastAPI(title="REST API", description="REST API solution for Adastra")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all tables if they don't exist
Base.metadata.create_all(bind=engine)


# Initialize the default admin user
def initialize_admin_user():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()


initialize_admin_user()

# Include API routers
app.include_router(auth.router, prefix=f"{settings.API_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_STR}/users", tags=["users"])
