from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Project(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    mentor_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    whatsapp_link = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    mentor = relationship("User")
