from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class LessonProgress(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
    lesson_id = Column(String, ForeignKey("lesson.id", ondelete="CASCADE"), index=True, nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    answers = Column(Text, nullable=True) # JSON string of quiz answers
    score = Column(Float, nullable=True)

    user = relationship("User")
    lesson = relationship("Lesson")
