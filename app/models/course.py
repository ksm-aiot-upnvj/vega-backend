from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Category(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    courses = relationship("Course", back_populates="category")

class Course(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category_id = Column(String, ForeignKey("category.id"))
    level = Column(String, default="BEGINNER")
    status = Column(String, default="DRAFT") # DRAFT, PUBLISHED
    mentor_id = Column(String, ForeignKey("user.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    category = relationship("Category", back_populates="courses")
    mentor = relationship("User")
    modules = relationship("Module", back_populates="course", cascade="all, delete-orphan", order_by="Module.order")
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

    @property
    def mentor_name(self) -> str:
        return self.mentor.name if self.mentor else "Unknown"

    @property
    def total_modules(self) -> int:
        return len(self.modules) if self.modules else 0

    @property
    def total_lessons(self) -> int:
        return sum(len(m.lessons) for m in self.modules) if self.modules else 0

    @property
    def enrolled_count(self) -> int:
        return len(self.enrollments) if self.enrollments else 0

    @property
    def estimated_duration(self) -> int:
        # Assuming each lesson is 10 minutes on average if not specified
        return sum(sum((l.duration or 10) for l in m.lessons) for m in self.modules) if self.modules else 0

class Module(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("course.id", ondelete="CASCADE"), index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, default=1)
    deadline = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="modules")
    lessons = relationship("Lesson", back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order")
    quizzes = relationship("Quiz", back_populates="module", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="module", cascade="all, delete-orphan")

class Lesson(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, ForeignKey("module.id", ondelete="CASCADE"), index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    lesson_type = Column(String, default="TEXT") # TEXT, VIDEO, IMAGE, FILE, LINK, TASK
    order = Column(Integer, default=1)
    duration = Column(Integer, default=0) # in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_completed = Column(Boolean, default=False) # For demo purpose, real completion should be tracked per user
    task_code = Column(String, nullable=True) # Secret code for TASK completion

    module = relationship("Module", back_populates="lessons")
