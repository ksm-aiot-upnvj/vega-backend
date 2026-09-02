from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import User

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    whatsapp_link: Optional[str] = None
    github_link: Optional[str] = None
    image_url: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    whatsapp_link: Optional[str] = None
    github_link: Optional[str] = None
    image_url: Optional[str] = None

class ProjectInDBBase(ProjectBase):
    id: str
    mentor_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Project(ProjectInDBBase):
    mentor: Optional[User] = None
