from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class AnnouncementBase(BaseModel):
    title: str
    description: str
    event_date: Optional[datetime] = None
    target_audience: str
    status: Optional[str] = "PUBLISHED"
    scheduled_at: Optional[datetime] = None

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    target_audience: Optional[str] = None
    status: Optional[str] = None
    scheduled_at: Optional[datetime] = None

class Announcement(AnnouncementBase):
    id: str
    mentor_id: str
    created_at: datetime
    author_name: Optional[str] = None
    is_notified: Optional[bool] = False

    class Config:
        from_attributes = True

class AnnouncementNotifyToggle(BaseModel):
    is_notified: bool
