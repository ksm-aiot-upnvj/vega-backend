from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.quiz import Quiz, Question, Option, QuizAttempt

class CRUDQuiz:
    def get(self, db: Session, id: str) -> Optional[Quiz]:
        return db.query(Quiz).filter(Quiz.id == id).first()

    def get_questions(self, db: Session, quiz_id: str) -> List[Question]:
        return db.query(Question).options(
            joinedload(Question.options)
        ).filter(Question.quiz_id == quiz_id).all()

    def create_attempt(self, db: Session, *, quiz_id: str, user_id: str, score: float, total_points: float, percentage: float, passed: bool) -> QuizAttempt:
        db_obj = QuizAttempt(
            quiz_id=quiz_id,
            user_id=user_id,
            score=score,
            total_points=total_points,
            percentage=percentage,
            passed=passed
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_quiz = CRUDQuiz()
