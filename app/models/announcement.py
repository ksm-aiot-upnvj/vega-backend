from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
import uuid
import enum

class TargetAudience(str, enum.Enum):
    ENROLLED_MEMBERS = "ENROLLED_MEMBERS"
    MENTORS = "MENTORS"
    BOTH = "BOTH"

class AnnouncementStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    SCHEDULED = "SCHEDULED"

class Announcement(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(DateTime(timezone=True), nullable=True)
    target_audience = Column(String, default=TargetAudience.ENROLLED_MEMBERS.value)
    status = Column(String, default=AnnouncementStatus.PUBLISHED.value)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    mentor_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    mentor = relationship("User")
    notifications = relationship("AnnouncementNotification", back_populates="announcement", cascade="all, delete-orphan")

class AnnouncementNotification(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    announcement_id = Column(String, ForeignKey("announcement.id", ondelete="CASCADE"), index=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True)
    is_notified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    announcement = relationship("Announcement", back_populates="notifications")
    user = relationship("User")
