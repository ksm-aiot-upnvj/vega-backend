from fastapi import APIRouter
from app.api.routers import auth, users, courses, categories, enrollments, quizzes, assignments, lessons, announcements

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(assignments.router, prefix="/assignments", tags=["assignments"])
api_router.include_router(announcements.router, prefix="/announcements", tags=["announcements"])
