import sys
from app.db.session import SessionLocal
from app import crud
from app.schemas.category import Category
from app.schemas.course import Course

db = SessionLocal()

try:
    categories = crud.crud_category.get_multi(db, skip=0, limit=100)
    for c in categories:
        Category.model_validate(c)
    print("Categories ok")
except Exception as e:
    print("Error in categories:", e)

try:
    courses = crud.crud_course.get_multi(db, skip=0, limit=100)
    for c in courses:
        Course.model_validate(c)
    print("Courses ok")
except Exception as e:
    print("Error in courses:", e)
