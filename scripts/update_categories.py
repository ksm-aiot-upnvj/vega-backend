import sys
from app.db.base import Base # Imports all models correctly
from app.db.session import SessionLocal
from app.models.course import Category

db = SessionLocal()

# Delete old categories
db.query(Category).delete()

# Insert new categories
categories = [
    {"name": "Internet of Things (IoT)", "slug": "internet-of-things-iot"},
    {"name": "Artificial Intelligence / Machine Learning", "slug": "ai-ml"},
    {"name": "Web & Cloud Systems", "slug": "web-cloud-systems"}
]

for cat in categories:
    db.add(Category(name=cat["name"], slug=cat["slug"]))

db.commit()
print("Categories updated successfully.")
