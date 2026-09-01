from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class User(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="MEMBER")
    nim = Column(String, nullable=True)
    program_studi = Column(String, nullable=True)
    semester = Column(String, nullable=True)
    name = Column(String, nullable=False)
    interest = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

