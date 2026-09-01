from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.course import Category

class CRUDCategory:
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Category]:
        return db.query(Category).offset(skip).limit(limit).all()

crud_category = CRUDCategory()
