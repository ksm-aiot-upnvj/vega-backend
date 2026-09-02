# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.user import User
from app.models.course import Course, Category, Module, Lesson
from app.models.enrollment import Enrollment
from app.models.quiz import Quiz, Question, Option, QuizAttempt
from app.models.assignment import Assignment, Submission
from app.models.progress import LessonProgress
from app.models.announcement import Announcement, AnnouncementNotification
