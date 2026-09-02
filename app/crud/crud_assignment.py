from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.assignment import Assignment, Submission

class CRUDAssignment:
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Assignment]:
        return db.query(Assignment).offset(skip).limit(limit).all()

    def get_by_course(self, db: Session, course_id: str) -> List[Assignment]:
        return db.query(Assignment).filter(Assignment.course_id == course_id).all()

    def get_submissions_by_user(self, db: Session, user_id: str) -> List[Submission]:
        return db.query(Submission).filter(Submission.user_id == user_id).all()

crud_assignment = CRUDAssignment()

