from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.schemas.category import Category
from app.schemas.module import Module

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    level: Optional[str] = "BEGINNER"
    status: Optional[str] = "DRAFT"

class CourseCreate(CourseBase):
    category_id: Optional[str] = None

class CourseUpdate(CourseBase):
    pass

class CourseInDBBase(CourseBase):
    id: str
    category_id: Optional[str] = None
    mentor_id: Optional[str] = None
    created_at: Optional[datetime] = None
    mentor_name: Optional[str] = "Unknown"
    estimated_duration: Optional[int] = 0
    total_modules: Optional[int] = 0
    total_lessons: Optional[int] = 0
    enrolled_count: Optional[int] = 0
    category: Optional[Category] = None

    class Config:
        from_attributes = True

class Course(CourseInDBBase):
    pass

class CourseWithModules(Course):
    modules: List[Module] = []

class LessonBuilder(BaseModel):
    id: Optional[str] = None
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    lesson_type: str = "TEXT"
    order: int
    task_code: Optional[str] = None

class ModuleBuilder(BaseModel):
    id: Optional[str] = None
    title: str
    order: int
    deadline: Optional[datetime] = None
    lessons: List[LessonBuilder] = []

class CourseBuilderPayload(BaseModel):
    modules: List[ModuleBuilder] = []
