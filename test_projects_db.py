from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.project import Project

db = SessionLocal()
try:
    print("Testing /my-members")
    # Simulate current_user is a mentor
    mentor = db.query(User).filter(User.role == "MENTOR").first()
    if mentor:
        print(f"Found mentor: {mentor.id}")
        members = db.query(User).filter(User.mentor_id == mentor.id).all()
        print(f"Found members: {len(members)}")
    else:
        print("No mentor found")

    print("Testing /projects/")
    if mentor:
        from app.crud import crud_project
        projects = crud_project.get_by_mentor(db, mentor_id=mentor.id)
        print(f"Found projects: {len(projects)}")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
