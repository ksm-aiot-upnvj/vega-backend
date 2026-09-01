from typing import Any, List, Dict
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.api import deps
from app.models.course import Lesson as LessonModel, Module as ModuleModel, Course as CourseModel
from app.models.progress import LessonProgress
from app.models.user import User
from datetime import datetime, timezone

router = APIRouter()

@router.get("/me/submissions", response_model=List[Dict])
def get_my_submissions(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"]))
) -> Any:
    """
    Get all lesson progress submissions across all courses taught by this mentor.
    """
    # Get all courses by this mentor (or all if admin)
    if current_user.role == "ADMIN":
        courses = db.query(CourseModel).all()
    else:
        courses = db.query(CourseModel).filter(CourseModel.mentor_id == current_user.id).all()

    if not courses:
        return []

    # Build lookup maps
    lesson_map: Dict[str, LessonModel] = {}
    module_map: Dict[str, ModuleModel] = {}
    course_map: Dict[str, CourseModel] = {}

    for course in courses:
        for module in course.modules:
            module_map[module.id] = module
            course_map[module.id] = course
            for lesson in module.lessons:
                lesson_map[lesson.id] = lesson

    if not lesson_map:
        return []

    progress_records = db.query(LessonProgress).filter(
        LessonProgress.lesson_id.in_(list(lesson_map.keys())),
        LessonProgress.is_completed == True
    ).order_by(LessonProgress.completed_at.desc()).all()

    # Eagerly load users to avoid lazy-loading None issue
    user_ids = list({p.user_id for p in progress_records})
    users = db.query(User).filter(User.id.in_(user_ids)).all()
    user_by_id = {u.id: u for u in users}

    result = []
    for p in progress_records:
        lesson = lesson_map.get(p.lesson_id)
        if not lesson:
            continue
        module = module_map.get(lesson.module_id)
        course = course_map.get(lesson.module_id)
        user = user_by_id.get(p.user_id)
        if not user:
            continue
        result.append({
            "submission_id": p.id,
            "user_id": p.user_id,
            "user_name": user.name,
            "user_email": user.email,
            "course_id": course.id if course else None,
            "course_title": course.title if course else "-",
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

@router.put("/me/submissions/{submission_id}/score", response_model=Dict)
def score_submission(
    submission_id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.RequireRole(["ADMIN", "MENTOR"])),
    score: float = Body(..., embed=True)
) -> Any:
    """
    Set a score for a submission (quiz/task answer).
    """
    progress = db.query(LessonProgress).filter(LessonProgress.id == submission_id).first()
    if not progress:
        raise HTTPException(status_code=404, detail="Submission not found")
    progress.score = score
    db.commit()
    return {"success": True, "score": score}

@router.post("/{id}/complete", response_model=dict)
def complete_lesson(
    id: str,
    task_code: str = Body(None, embed=True),
    answers: str = Body(None, embed=True),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Complete a lesson. If lesson_type is TASK, task_code must match.
    Blocked if module deadline has passed.
    """
    lesson = db.query(LessonModel).filter(LessonModel.id == id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Check module deadline
    module = db.query(ModuleModel).filter(ModuleModel.id == lesson.module_id).first()
    if module and module.deadline:
        now = datetime.now(timezone.utc)
        deadline = module.deadline
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        if now > deadline:
            raise HTTPException(status_code=403, detail="Deadline modul ini sudah lewat")

    if lesson.lesson_type == "TASK":
        if not task_code:
            raise HTTPException(status_code=400, detail="Task code is required")
        if task_code != lesson.task_code:
            raise HTTPException(status_code=400, detail="Kode tugas tidak valid")

    # Check if already completed
    progress = db.query(LessonProgress).filter(
        LessonProgress.lesson_id == id,
        LessonProgress.user_id == current_user.id
    ).first()

    if progress:
        progress.is_completed = True
        progress.completed_at = func.now()
        if answers:
            progress.answers = answers
    else:
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=id,
            is_completed=True,
            completed_at=func.now(),
            answers=answers
        )
        db.add(progress)
        
    db.commit()
    return {"success": True, "message": "Berhasil menyelesaikan lesson"}
