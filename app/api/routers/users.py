from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.user import User, UserUpdate
from app.models.user import User as UserModel
from app.core.security import verify_password, get_password_hash

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user

@router.get("/", response_model=list[User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.RequireRole(["ADMIN"]))
) -> Any:
    """
    Retrieve users. Admin only.
    """
    from app import crud
    users = crud.crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    from app import crud
    user = crud.crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.put("/password", response_model=User)
def update_password(
    *,
    db: Session = Depends(deps.get_db),
    old_password: str = Body(...),
    new_password: str = Body(...),
    current_user: UserModel = Depends(deps.get_current_user),
) -> Any:
    """
    Update own password.
    """
    from app import crud
    if not verify_password(old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Password lama salah")
    
    hashed_password = get_password_hash(new_password)
    current_user.hashed_password = hashed_password
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/{user_id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    user_in: UserUpdate,
    current_user: UserModel = Depends(deps.RequireRole(["ADMIN"])),
) -> Any:
    """
    Update a user.
    """
    from app import crud
    user = crud.crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.crud_user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: str,
    current_user: UserModel = Depends(deps.RequireRole(["ADMIN"])),
) -> Any:
    """
    Delete a user.
    """
    from app import crud
    user = crud.crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = crud.crud_user.remove(db, id=user_id)
    return user
