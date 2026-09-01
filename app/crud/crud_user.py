from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get(db: Session, id: str) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()

def create(db: Session, obj_in: UserCreate) -> User:
    db_obj = User(
        email=obj_in.email,
        password_hash=get_password_hash(obj_in.password),
        name=obj_in.name,
        role=obj_in.role or "MEMBER",
        nim=obj_in.nim,
        interest=obj_in.interest
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
