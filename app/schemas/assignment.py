from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[float] = 100.0
    accepted_types: Optional[List[str]] = []

class AssignmentCreate(AssignmentBase):
    course_id: str
    module_id: str

class AssignmentInDBBase(AssignmentBase):
    id: str
    course_id: str
    module_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Assignment(AssignmentInDBBase):
    course_title: Optional[str] = None

class SubmissionBase(BaseModel):
    submission_type: str
    file_url: Optional[str] = None
    github_url: Optional[str] = None
    url: Optional[str] = None
    notes: Optional[str] = None

class SubmissionCreate(SubmissionBase):
    assignment_id: str

class SubmissionInDBBase(SubmissionBase):
    id: str
    assignment_id: str
    user_id: str
    status: Optional[str] = "SUBMITTED"
    score: Optional[float] = None
    feedback: Optional[str] = None
    submitted_at: Optional[datetime] = None
    graded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Submission(SubmissionInDBBase):
    pass

class AssignmentWithSubmission(Assignment):
    submission: Optional[Submission] = None
