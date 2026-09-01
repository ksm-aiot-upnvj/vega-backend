from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.course import Course

class EnrollmentBase(BaseModel):
    course_id: str

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentUpdate(BaseModel):
    progress_percentage: Optional[float] = None
    completed_lessons: Optional[int] = None
    status: Optional[str] = None

class EnrollmentInDBBase(EnrollmentBase):
    id: str
    user_id: str
    progress_percentage: Optional[float] = 0.0
    completed_lessons: Optional[int] = 0
    total_lessons: Optional[int] = 0
    status: Optional[str] = "ACTIVE"
    enrolled_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Enrollment(EnrollmentInDBBase):
    course: Optional[Course] = None
