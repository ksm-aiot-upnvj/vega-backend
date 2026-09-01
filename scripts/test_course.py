import sys
from app.db.session import SessionLocal
from app import crud
from app.schemas.course import CourseCreate, Course
from app.schemas.user import User

db = SessionLocal()
# find a mentor
mentor = db.query(crud.crud_user.User).filter_by(role="MENTOR").first()

try:
    course_in = CourseCreate(title="Test Course", description="Test", level="BEGINNER", category_id=None)
    course = crud.crud_course.create_with_owner(db=db, obj_in=course_in, mentor_id=mentor.id)
    Course.model_validate(course)
    print("Course created successfully")
except Exception as e:
    print('Error:', e)
