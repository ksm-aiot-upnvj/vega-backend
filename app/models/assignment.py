from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Assignment(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("course.id", ondelete="CASCADE"), index=True)
    module_id = Column(String, ForeignKey("module.id", ondelete="CASCADE"), index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    max_score = Column(Float, default=100.0)
    accepted_types = Column(JSON, default=list) # e.g., ["FILE", "GITHUB", "URL"]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="assignments")
    module = relationship("Module", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")

class Submission(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    assignment_id = Column(String, ForeignKey("assignment.id", ondelete="CASCADE"), index=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True)
    submission_type = Column(String, nullable=False) # FILE, GITHUB, URL
    file_url = Column(String, nullable=True)
    github_url = Column(String, nullable=True)
    url = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String, default="SUBMITTED") # SUBMITTED, GRADED
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    graded_at = Column(DateTime(timezone=True), nullable=True)

    assignment = relationship("Assignment", back_populates="submissions")
    user = relationship("User")
