from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid

class Quiz(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    course_id = Column(String, ForeignKey("course.id", ondelete="CASCADE"), index=True)
    module_id = Column(String, ForeignKey("module.id", ondelete="CASCADE"), index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    time_limit = Column(Integer, default=0) # in minutes
    passing_score = Column(Float, default=70.0)
    total_questions = Column(Integer, default=0)
    is_final = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    course = relationship("Course", back_populates="quizzes")
    module = relationship("Module", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan", order_by="Question.order")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")

class Question(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, ForeignKey("quiz.id", ondelete="CASCADE"), index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, default="MULTIPLE_CHOICE")
    order = Column(Integer, default=1)
    points = Column(Integer, default=10)

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan", order_by="Option.order")

class Option(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    question_id = Column(String, ForeignKey("question.id", ondelete="CASCADE"), index=True)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    order = Column(Integer, default=1)

    question = relationship("Question", back_populates="options")

class QuizAttempt(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, ForeignKey("quiz.id", ondelete="CASCADE"), index=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True)
    score = Column(Float, default=0.0)
    total_points = Column(Float, default=0.0)
    percentage = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

    quiz = relationship("Quiz", back_populates="attempts")
    user = relationship("User")
