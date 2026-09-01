from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.quiz import Quiz, Question, QuizAttemptCreate, QuizResult
from app import crud
from app.models.user import User

router = APIRouter()

@router.get("/{id}", response_model=Quiz)
def read_quiz(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    quiz = crud.crud_quiz.get(db, id=id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.get("/{id}/questions", response_model=List[Question])
def read_quiz_questions(
    id: str,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    quiz = crud.crud_quiz.get(db, id=id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return crud.crud_quiz.get_questions(db, quiz_id=id)

@router.post("/{id}/submit", response_model=QuizResult)
def submit_quiz(
    id: str,
    *,
    db: Session = Depends(deps.get_db),
    attempt_in: QuizAttemptCreate,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    quiz = crud.crud_quiz.get(db, id=id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Check score and create attempt
    attempt = crud.crud_quiz.create_attempt(
        db,
        quiz_id=id,
        user_id=current_user.id,
        score=attempt_in.score,
        total_points=attempt_in.total_points,
        percentage=attempt_in.percentage,
        passed=attempt_in.passed
    )
    return {
        "id": attempt.id,
        "quiz_id": attempt.quiz_id,
        "user_id": attempt.user_id,
        "score": attempt.score,
        "total_points": attempt.total_points,
        "percentage": attempt.percentage,
        "passed": attempt.passed,
        "submitted_at": attempt.submitted_at,
        "quiz_title": quiz.title
    }
