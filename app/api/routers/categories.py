from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.category import Category
from app import crud

router = APIRouter()

@router.get("/", response_model=List[Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories.
    """
    return crud.crud_category.get_multi(db, skip=skip, limit=limit)
