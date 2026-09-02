import sys
from pathlib import Path

# Add the parent directory to sys.path to allow imports from app
current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))

from app.db.session import engine
from app.db.base import Base

def migrate():
    print("Creating all missing tables...")
    Base.metadata.create_all(bind=engine)
    print("Done!")

if __name__ == "__main__":
    migrate()
