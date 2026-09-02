import sqlite3
import os

db_path = "vega.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE announcement ADD COLUMN status VARCHAR DEFAULT 'PUBLISHED'")
        print("Added status column.")
    except sqlite3.OperationalError as e:
        print(f"Error adding status: {e}")
        
    try:
        cursor.execute("ALTER TABLE announcement ADD COLUMN scheduled_at DATETIME")
        print("Added scheduled_at column.")
    except sqlite3.OperationalError as e:
        print(f"Error adding scheduled_at: {e}")
        
    conn.commit()
    conn.close()
else:
    print(f"{db_path} not found.")
