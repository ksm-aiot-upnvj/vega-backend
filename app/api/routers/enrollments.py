from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.enrollment import Enrollment, EnrollmentCreate
from app import crud
from app.models.user import User

router = APIRouter()

@router.get("/me", response_model=List[Enrollment])
def read_my_enrollments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Retrieve enrollments for current user.
    """
    return crud.crud_enrollment.get_by_user(db, user_id=current_user.id)

@router.post("/", response_model=Enrollment)
def enroll_course(
    *,
    db: Session = Depends(deps.get_db),
    enrollment_in: EnrollmentCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Enroll in a course.
    """
    existing = crud.crud_enrollment.get_by_user_and_course(
        db, user_id=current_user.id, course_id=enrollment_in.course_id
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    return crud.crud_enrollment.create(db, obj_in=enrollment_in, user_id=current_user.id)
