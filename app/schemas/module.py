from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.schemas.lesson import Lesson

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    order: Optional[int] = 1
    deadline: Optional[datetime] = None

class ModuleCreate(ModuleBase):
    course_id: str

class ModuleUpdate(ModuleBase):
    title: Optional[str] = None

class ModuleInDBBase(ModuleBase):
    id: str
    course_id: str
    created_at: Optional[datetime] = None
    deadline: Optional[datetime] = None

    class Config:
        from_attributes = True

class Module(ModuleInDBBase):
    lessons: List[Lesson] = []
