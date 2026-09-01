from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.assignment import Assignment
from app import crud
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[Assignment])
def read_assignments(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    return crud.crud_assignment.get_multi(db, skip=skip, limit=limit)
