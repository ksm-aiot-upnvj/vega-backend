from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class LessonBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    lesson_type: Optional[str] = "TEXT"
    order: Optional[int] = 1
    duration: Optional[int] = 0
    task_code: Optional[str] = None

class LessonCreate(LessonBase):
    module_id: str

class LessonUpdate(LessonBase):
    title: Optional[str] = None

class LessonInDBBase(LessonBase):
    id: str
    module_id: str
    created_at: Optional[datetime] = None
    is_completed: Optional[bool] = False

    class Config:
        from_attributes = True

class Lesson(LessonInDBBase):
    pass
