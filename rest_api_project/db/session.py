from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Get database constants
user = settings.DATABASE_USER
password = settings.DATABASE_PASSWORD
host = settings.DATABASE_HOST
port = settings.DATABASE_PORT
db = settings.DATABASE_NAME

# Create database URL
url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
print(f"URL->{url}")

# Create session
engine = create_engine(url, pool_size=settings.DATABASE_POOL_SIZE, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
