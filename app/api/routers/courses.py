from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.course import Course, CourseCreate, CourseWithModules, CourseBuilderPayload
from app import crud
from app.models.user import User
from app.models.course import Module as ModuleModel, Lesson as LessonModel
from app.models.progress import LessonProgress
from app.models.enrollment import Enrollment
import uuid

router = APIRouter()

@router.get("/", response_model=List[Course])
def read_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User | None = Depends(deps.get_current_user_optional)
) -> Any:
    """
    Retrieve courses.
    """
    courses = crud.crud_course.get_multi(db, skip=skip, limit=limit)
    if not current_user or current_user.role == "MEMBER":
        courses = [c for c in courses if c.status == "PUBLISHED"]
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

@router.get("/{id}/progress", response_model=Dict)
def get_course_progress(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get current user's lesson progress for a course.
    Returns a dict: {lesson_id: {is_completed, completed_at, answers}}
    """
    # Get all lessons in this course
    course = crud.crud_course.get(db, id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    lesson_ids = [
        l.id
        for m in course.modules
        for l in m.lessons
    ]

    if not lesson_ids:
        return {}

    progress_records = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id.in_(lesson_ids)
    ).all()

    result = {}
    for p in progress_records:
        result[p.lesson_id] = {
            "is_completed": p.is_completed,
            "completed_at": p.completed_at.isoformat() if p.completed_at else None,
            "answers": p.answers,
            "score": p.score,
        }
    return result

@router.get("/{id}/submissions", response_model=List[Dict])
def get_course_submissions(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Get all lesson progress submissions for a course (mentor/admin only).
    """
    course = crud.crud_course.get(db, id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    if current_user.role != "ADMIN" and course.mentor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    lesson_ids = [l.id for m in course.modules for l in m.lessons]
    lesson_map = {l.id: l for m in course.modules for l in m.lessons}
    module_map = {m.id: m for m in course.modules}

    if not lesson_ids:
        return []

    progress_records = db.query(LessonProgress).filter(
        LessonProgress.lesson_id.in_(lesson_ids),
        LessonProgress.is_completed == True
    ).all()

    result = []
    for p in progress_records:
        lesson = lesson_map.get(p.lesson_id)
        user = p.user
        if not lesson or not user:
            continue
        module_id = lesson.module_id
        module = module_map.get(module_id)
        result.append({
            "user_id": p.user_id,
            "user_name": user.name,
            "user_email": user.email,
            "lesson_id": p.lesson_id,
            "lesson_title": lesson.title,
            "lesson_type": lesson.lesson_type,
            "module_title": module.title if module else "-",
            "is_completed": p.is_completed,
            "completed_at": p.completed_at.isoformat() if p.completed_at else None,
            "answers": p.answers,
            "score": p.score,
        })
    return result

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

@router.delete("/{id}", response_model=Course)
def delete_course(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Delete course by ID.
    """
    course = crud.crud_course.get(db, id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    if current_user.role != "ADMIN" and course.mentor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this course")
    
    course = crud.crud_course.remove(db, id=id)
    return course

@router.put("/{id}/publish", response_model=Course)
def publish_course(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Publish course by ID.
    """
    course = crud.crud_course.get(db, id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user.role != "ADMIN" and course.mentor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to publish this course")
    
    course.status = "PUBLISHED"
    db.commit()
    db.refresh(course)
    return course

@router.put("/{id}/builder", response_model=CourseWithModules)
def update_course_builder(
    id: str,
    payload: CourseBuilderPayload,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Update course modules and lessons (builder).
    """
    course = crud.crud_course.get(db, id=id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if current_user.role != "ADMIN" and course.mentor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this course")
    
    # Load and delete existing modules (cascades to lessons)
    existing_modules = db.query(ModuleModel).filter(ModuleModel.course_id == id).all()
    for mod in existing_modules:
        db.delete(mod)
    db.flush()  # flush deletes before inserts to avoid FK conflicts
    
    # Re-insert modules and lessons
    for m in payload.modules:
        mod_id = m.id if m.id and not str(m.id).isdigit() else str(uuid.uuid4())
        mod = ModuleModel(
            id=mod_id,
            course_id=id,
            title=m.title,
            order=m.order,
            deadline=m.deadline
        )
        db.add(mod)
        db.flush()  # ensure mod.id is set before referencing in lessons
        
        for l in m.lessons:
            lesson_id = l.id if l.id and not str(l.id).isdigit() and not str(l.id).startswith('l') else str(uuid.uuid4())
            lesson = LessonModel(
                id=lesson_id,
                module_id=mod.id,
                title=l.title,
                description=l.description,
                content=l.content,
                lesson_type=l.lesson_type,
                order=l.order,
                task_code=l.task_code if l.lesson_type == "TASK" else None
            )
            db.add(lesson)
            
    db.commit()
    db.refresh(course)
    return course
