from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.course import Course, CourseCreate, CourseWithModules
from app import crud
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Course])
def read_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve courses.
    """
    courses = crud.crud_course.get_multi(db, skip=skip, limit=limit)
    return courses

@router.get("/{id}", response_model=CourseWithModules)
def read_course(
    id: str,
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get course by ID.
    """
    course = crud.crud_course.get(db, id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/", response_model=Course)
def create_course(
    *,
    db: Session = Depends(deps.get_db),
    course_in: CourseCreate,
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Create new course. Requires ADMIN or MENTOR role.
    """
    course = crud.crud_course.create_with_owner(db=db, obj_in=course_in, mentor_id=current_user.id)
    return course
