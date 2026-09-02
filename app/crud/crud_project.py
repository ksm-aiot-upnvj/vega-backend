from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

def get(db: Session, id: str) -> Optional[Project]:
    return db.query(Project).filter(Project.id == id).first()

def get_by_mentor(db: Session, *, mentor_id: str, skip: int = 0, limit: int = 100) -> List[Project]:
    return db.query(Project).filter(Project.mentor_id == mentor_id).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()

def create(db: Session, obj_in: ProjectCreate, mentor_id: str) -> Project:
    db_obj = Project(
        mentor_id=mentor_id,
        title=obj_in.title,
        description=obj_in.description,
        whatsapp_link=obj_in.whatsapp_link,
        github_link=obj_in.github_link,
        image_url=obj_in.image_url,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update(db: Session, *, db_obj: Project, obj_in: ProjectUpdate) -> Project:
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: str) -> Project:
    obj = db.query(Project).get(id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj
