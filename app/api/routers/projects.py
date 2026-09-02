from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.project import Project, ProjectCreate, ProjectUpdate
from app.models.user import User as UserModel
from app.schemas.user import User as UserSchema

router = APIRouter()

@router.get("/my-group", response_model=List[Project])
def read_my_group_projects(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Get projects created by the mentor of the current user.
    """
    if not current_user.mentor_id:
        return []
    
    from app import crud
    projects = crud.crud_project.get_by_mentor(db, mentor_id=current_user.mentor_id)
    return projects

@router.get("/my-peers", response_model=List[UserSchema])
def read_my_peers(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Get peers in the same group (same mentor).
    """
    if not current_user.mentor_id:
        return []
    
    peers = db.query(UserModel).filter(UserModel.mentor_id == current_user.mentor_id).all()
    return peers

@router.get("/my-mentor", response_model=UserSchema)
def read_my_mentor(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.get_current_user)
) -> Any:
    """
    Get my mentor.
    """
    if not current_user.mentor_id:
        raise HTTPException(status_code=404, detail="No mentor assigned")
    
    from app import crud
    mentor = crud.crud_user.get(db, id=current_user.mentor_id)
    return mentor

@router.get("/my-members", response_model=List[UserSchema])
def read_my_members(
    db: Session = Depends(deps.get_db),
    current_user: UserModel = Depends(deps.RequireRole(["MENTOR"]))
) -> Any:
    """
    Get members assigned to this mentor. Mentor only.
    """
    members = db.query(UserModel).filter(UserModel.mentor_id == current_user.id).all()
    return members

@router.get("/", response_model=List[Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(deps.RequireRole(["MENTOR"]))
) -> Any:
    """
    Retrieve projects created by this mentor. Mentor only.
    """
    from app import crud
    projects = crud.crud_project.get_by_mentor(db, mentor_id=current_user.id, skip=skip, limit=limit)
    return projects

@router.post("/", response_model=Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: ProjectCreate,
    current_user: UserModel = Depends(deps.RequireRole(["MENTOR"]))
) -> Any:
    """
    Create new project. Mentor only.
    """
    from app import crud
    project = crud.crud_project.create(db, obj_in=project_in, mentor_id=current_user.id)
    return project

@router.put("/{id}", response_model=Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    project_in: ProjectUpdate,
    current_user: UserModel = Depends(deps.RequireRole(["MENTOR"]))
) -> Any:
    """
    Update a project. Mentor only.
    """
    from app import crud
    project = crud.crud_project.get(db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.mentor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project = crud.crud_project.update(db, db_obj=project, obj_in=project_in)
    return project

@router.delete("/{id}", response_model=Project)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: UserModel = Depends(deps.RequireRole(["MENTOR"]))
) -> Any:
    """
    Delete a project. Mentor only.
    """
    from app import crud
    project = crud.crud_project.get(db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.mentor_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    project = crud.crud_project.remove(db, id=id)
    return project
