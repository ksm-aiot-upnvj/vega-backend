from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.announcement import Announcement, AnnouncementCreate, AnnouncementUpdate, AnnouncementNotifyToggle
from app.models.announcement import Announcement as AnnouncementModel, AnnouncementNotification, TargetAudience, AnnouncementStatus
from app.models.user import User
from app.models.course import Course
from app.models.enrollment import Enrollment

router = APIRouter()

@router.get("/", response_model=List[Announcement])
def get_announcements(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get announcements relevant to the current user.
    """
    from sqlalchemy import or_
    import datetime

    now = datetime.datetime.now(datetime.timezone.utc)

    if current_user.role in ("ADMIN", "MENTOR"):
        # Mentors see their own announcements (all statuses)
        # And announcements targeted to MENTORS or BOTH (only PUBLISHED or SCHEDULED that are past due)
        announcements = db.query(AnnouncementModel).filter(
            or_(
                AnnouncementModel.mentor_id == current_user.id,
                (AnnouncementModel.target_audience.in_([TargetAudience.MENTORS.value, TargetAudience.BOTH.value])) &
                (
                    (AnnouncementModel.status == AnnouncementStatus.PUBLISHED.value) |
                    ((AnnouncementModel.status == AnnouncementStatus.SCHEDULED.value) & (AnnouncementModel.scheduled_at <= now))
                )
            )
        ).order_by(AnnouncementModel.created_at.desc()).all()
    else:
        # Members see announcements targeted to ENROLLED_MEMBERS or BOTH,
        # only PUBLISHED or SCHEDULED that are past due.
        enrolled_mentor_ids = db.query(Course.mentor_id).join(
            Enrollment, Enrollment.course_id == Course.id
        ).filter(Enrollment.user_id == current_user.id).subquery()

        announcements = db.query(AnnouncementModel).filter(
            (
                (
                    (AnnouncementModel.target_audience.in_([TargetAudience.ENROLLED_MEMBERS.value, TargetAudience.BOTH.value]) & AnnouncementModel.mentor_id.in_(enrolled_mentor_ids))
                    | (AnnouncementModel.target_audience == TargetAudience.BOTH.value)
                )
            ) & (
                (AnnouncementModel.status == AnnouncementStatus.PUBLISHED.value) |
                ((AnnouncementModel.status == AnnouncementStatus.SCHEDULED.value) & (AnnouncementModel.scheduled_at <= now))
            )
        ).order_by(AnnouncementModel.created_at.desc()).all()

    # Fetch notifications to attach is_notified status
    notification_map = {}
    if announcements:
        announcement_ids = [a.id for a in announcements]
        notifications = db.query(AnnouncementNotification).filter(
            AnnouncementNotification.user_id == current_user.id,
            AnnouncementNotification.announcement_id.in_(announcement_ids)
        ).all()
        notification_map = {n.announcement_id: n.is_notified for n in notifications}

    output = []
    for a in announcements:
        output.append({
            "id": a.id,
            "title": a.title,
            "description": a.description,
            "event_date": a.event_date,
            "target_audience": a.target_audience,
            "status": a.status or "PUBLISHED",
            "scheduled_at": a.scheduled_at,
            "mentor_id": a.mentor_id,
            "created_at": a.created_at,
            "author_name": a.mentor.name if a.mentor else "Unknown",
            "is_notified": notification_map.get(a.id, False)
        })
    return output

@router.post("/", response_model=Announcement)
def create_announcement(
    *,
    db: Session = Depends(deps.get_db),
    announcement_in: AnnouncementCreate,
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Create a new announcement.
    """
    announcement = AnnouncementModel(
        title=announcement_in.title,
        description=announcement_in.description,
        event_date=announcement_in.event_date,
        target_audience=announcement_in.target_audience,
        status=announcement_in.status,
        scheduled_at=announcement_in.scheduled_at,
        mentor_id=current_user.id
    )
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    
    return {
        "id": announcement.id,
        "title": announcement.title,
        "description": announcement.description,
        "event_date": announcement.event_date,
        "target_audience": announcement.target_audience,
        "status": announcement.status,
        "scheduled_at": announcement.scheduled_at,
        "mentor_id": announcement.mentor_id,
        "created_at": announcement.created_at,
        "author_name": current_user.name,
        "is_notified": False
    }

@router.post("/{id}/notify")
def toggle_notify(
    id: str,
    payload: AnnouncementNotifyToggle,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Toggle is_notified for an announcement.
    """
    announcement = db.query(AnnouncementModel).filter(AnnouncementModel.id == id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
        
    notification = db.query(AnnouncementNotification).filter(
        AnnouncementNotification.announcement_id == id,
        AnnouncementNotification.user_id == current_user.id
    ).first()
    
    if notification:
        notification.is_notified = payload.is_notified
    else:
        notification = AnnouncementNotification(
            announcement_id=id,
            user_id=current_user.id,
            is_notified=payload.is_notified
        )
        db.add(notification)
        
    db.commit()
    return {"status": "success", "is_notified": payload.is_notified}

@router.put("/{id}", response_model=Announcement)
def update_announcement(
    *,
    id: str,
    db: Session = Depends(deps.get_db),
    announcement_in: AnnouncementUpdate,
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Update an announcement.
    """
    announcement = db.query(AnnouncementModel).filter(AnnouncementModel.id == id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
        
    if announcement.mentor_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    update_data = announcement_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(announcement, field, value)
        
    db.add(announcement)
    db.commit()
    db.refresh(announcement)
    
    return {
        "id": announcement.id,
        "title": announcement.title,
        "description": announcement.description,
        "event_date": announcement.event_date,
        "target_audience": announcement.target_audience,
        "status": announcement.status,
        "scheduled_at": announcement.scheduled_at,
        "mentor_id": announcement.mentor_id,
        "created_at": announcement.created_at,
        "author_name": current_user.name,
        "is_notified": False
    }

@router.delete("/{id}")
def delete_announcement(
    *,
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Delete an announcement.
    """
    announcement = db.query(AnnouncementModel).filter(AnnouncementModel.id == id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
        
    if announcement.mentor_id != current_user.id and current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    db.delete(announcement)
    db.commit()
    return {"status": "success"}
