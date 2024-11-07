from sqlalchemy import Column, String, Boolean
from db.session import Base
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class Token(Base):
    __tablename__ = "access_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    token = Column(String, unique=True, index=True, nullable=False)
    exp = Column(String, nullable=False)
    is_revoked = Column(Boolean, default=False)
