import sys
from app.db.session import SessionLocal
from app import crud
from app.schemas.user import User

db = SessionLocal()
users = crud.crud_user.get_multi(db, skip=0, limit=100)
for u in users:
    try:
        User.model_validate(u)
    except Exception as e:
        print('Error on user:', u.email)
        print(e)
        break
