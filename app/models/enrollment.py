from sqlalchemy import Column, String, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Enrollment(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id"), index=True)
    course_id = Column(String, ForeignKey("course.id"), index=True)
    progress_percentage = Column(Float, default=0.0)
    completed_lessons = Column(Integer, default=0)
    total_lessons = Column(Integer, default=0)
    status = Column(String, default="ACTIVE") # ACTIVE, COMPLETED, DROPPED
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    course = relationship("Course")
