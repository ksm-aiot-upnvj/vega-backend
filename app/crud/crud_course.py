from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.course import Course, Category, Module, Lesson
from app.schemas.course import CourseCreate

class CRUDCourse:
    def get(self, db: Session, id: str) -> Optional[Course]:
        # Include modules and lessons, mentor, category
        return db.query(Course).options(
            joinedload(Course.category),
            joinedload(Course.mentor),
            joinedload(Course.modules).joinedload(Module.lessons)
        ).filter(Course.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Course]:
        return db.query(Course).options(
            joinedload(Course.category),
            joinedload(Course.mentor)
        ).offset(skip).limit(limit).all()

    def create_with_owner(
        self, db: Session, *, obj_in: CourseCreate, mentor_id: str
    ) -> Course:
        db_obj = Course(
            title=obj_in.title,
            description=obj_in.description,
            level=obj_in.level,
            status=obj_in.status,
            category_id=obj_in.category_id,
            mentor_id=mentor_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str) -> Course:
        obj = db.query(Course).get(id)
        db.delete(obj)
        db.commit()
        return obj

crud_course = CRUDCourse()
