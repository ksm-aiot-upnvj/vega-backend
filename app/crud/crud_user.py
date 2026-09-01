from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
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

def get_multi(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def update(db: Session, *, db_obj: User, obj_in: dict | UserUpdate) -> User:
    if isinstance(obj_in, dict):
        update_data = obj_in
    else:
        update_data = obj_in.model_dump(exclude_unset=True)
    
    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["password_hash"] = hashed_password
        
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def remove(db: Session, *, id: str) -> User:
    obj = db.query(User).get(id)
    db.delete(obj)
    db.commit()
    return obj

