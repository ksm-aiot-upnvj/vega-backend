from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class OptionBase(BaseModel):
    option_text: str
    is_correct: Optional[bool] = False
    order: int = 1

class OptionCreate(OptionBase):
    pass

class OptionInDBBase(OptionBase):
    id: str
    question_id: str

    class Config:
        from_attributes = True

class Option(OptionInDBBase):
    pass

class QuestionBase(BaseModel):
    question_text: str
    question_type: Optional[str] = "MULTIPLE_CHOICE"
    order: int = 1
    points: int = 10

class QuestionCreate(QuestionBase):
    options: List[OptionCreate] = []

class QuestionInDBBase(QuestionBase):
    id: str
    quiz_id: str

    class Config:
        from_attributes = True

class Question(QuestionInDBBase):
    options: List[Option] = []

class QuizBase(BaseModel):
    title: str
    description: Optional[str] = None
    time_limit: Optional[int] = 0
    passing_score: Optional[float] = 70.0
    total_questions: Optional[int] = 0
    is_final: Optional[bool] = False

class QuizCreate(QuizBase):
    course_id: str
    module_id: str

class QuizInDBBase(QuizBase):
    id: str
    course_id: str
    module_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Quiz(QuizInDBBase):
    pass

class QuizAttemptBase(BaseModel):
    score: float
    total_points: float
    percentage: float
    passed: bool

class QuizAttemptCreate(QuizAttemptBase):
    quiz_id: str

class QuizAttemptInDBBase(QuizAttemptBase):
    id: str
    quiz_id: str
    user_id: str
    submitted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class QuizResult(QuizAttemptInDBBase):
    quiz_title: str
