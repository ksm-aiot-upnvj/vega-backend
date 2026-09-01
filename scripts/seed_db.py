import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.models.course import Course, Category
from app.core.security import get_password_hash
import uuid

def seed():
    db: Session = SessionLocal()
    try:
        # Create categories
        cat1 = Category(name="IoT Fundamentals", slug="iot-fundamentals")
        cat2 = Category(name="Artificial Intelligence", slug="artificial-intelligence")
        db.add_all([cat1, cat2])
        db.commit()

        # Create Users (Admin, Mentor, Member)
        admin = User(
            email="aiot@upnvj.ac.id",
            password_hash=get_password_hash("six faced world"),
            name="Vega Admin",
            role="ADMIN",
            nim="0000000000",
            interest="System Administration"
        )
        mentor = User(
            email="2310511042@mahasiswa.upnvj.ac.id",
            password_hash=get_password_hash("aiotupnvj2026"),
            name="Budi Mentor",
            role="MENTOR",
            nim="2310511042",
            interest="IoT Development"
        )
        member = User(
            email="2510511172@mahasiswa.upnvj.ac.id",
            password_hash=get_password_hash("aiotupnvj2026"),
            name="Andi Student",
            role="MEMBER",
            nim="2510511172",
            interest="Machine Learning"
        )
        db.add_all([admin, mentor, member])
        db.commit()
        db.refresh(cat1)
        db.refresh(mentor)

        # Create some courses
        course1 = Course(
            title="Introduction to ESP32",
            description="Learn the basics of ESP32 microcontroller programming.",
            level="BEGINNER",
            status="PUBLISHED",
            category_id=cat1.id,
            mentor_id=mentor.id
        )
        db.add(course1)
        db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
