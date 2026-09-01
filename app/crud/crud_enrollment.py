from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate

class CRUDEnrollment:
    def get_by_user(self, db: Session, user_id: str) -> List[Enrollment]:
        return db.query(Enrollment).options(
            joinedload(Enrollment.course)
        ).filter(Enrollment.user_id == user_id).all()

    def get_by_user_and_course(self, db: Session, user_id: str, course_id: str) -> Optional[Enrollment]:
        return db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()

    def create(self, db: Session, *, obj_in: EnrollmentCreate, user_id: str) -> Enrollment:
        db_obj = Enrollment(
            course_id=obj_in.course_id,
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_enrollment = CRUDEnrollment()
