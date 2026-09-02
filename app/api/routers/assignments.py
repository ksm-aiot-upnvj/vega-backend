from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.assignment import Assignment, AssignmentWithSubmission
from app import crud
from app.models.user import User
from app.models.assignment import Assignment as AssignmentModel
from app.models.enrollment import Enrollment
from app.models.course import Course

router = APIRouter()

@router.get("/", response_model=List[AssignmentWithSubmission])
def read_assignments(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Returns assignments relevant to the current user:
    - MEMBER: assignments from courses they are enrolled in
    - MENTOR/ADMIN: all assignments from their own courses
    """
    if current_user.role in ("MENTOR", "ADMIN"):
        # Get assignments from courses owned by this mentor
        results = (
            db.query(AssignmentModel)
            .join(Course, Course.id == AssignmentModel.course_id)
            .filter(Course.mentor_id == current_user.id)
            .all()
        )
    else:
        # Get assignments from enrolled courses
        enrolled_course_ids = (
            db.query(Enrollment.course_id)
            .filter(Enrollment.user_id == current_user.id)
            .subquery()
        )
        results = (
            db.query(AssignmentModel)
            .filter(AssignmentModel.course_id.in_(enrolled_course_ids))
            .all()
        )

    # Attach course_title and empty submission for schema compatibility
    output = []
    for a in results:
        course = db.query(Course).filter(Course.id == a.course_id).first()
        item = AssignmentWithSubmission(
            id=a.id,
            course_id=a.course_id,
            module_id=a.module_id,
            title=a.title,
            description=a.description or "",
            instructions=a.instructions,
            due_date=a.due_date,
            max_score=a.max_score or 100.0,
            accepted_types=a.accepted_types or [],
            created_at=a.created_at,
            course_title=course.title if course else "",
            submission=None,
        )
        output.append(item)
    return output

@router.get("/course/{course_id}", response_model=List[Assignment])
def read_assignments_by_course(
    course_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """Get all assignments for a specific course. Used by mentor dashboard calendar."""
    return crud.crud_assignment.get_by_course(db, course_id=course_id)
