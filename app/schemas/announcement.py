from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class AnnouncementBase(BaseModel):
    title: str
    description: str
    event_date: Optional[datetime] = None
    target_audience: str

class AnnouncementCreate(AnnouncementBase):
    pass

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
