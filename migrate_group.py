import sqlite3

def migrate():
    conn = sqlite3.connect("vega.db")
    cursor = conn.cursor()

    # Add mentor_id to user
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN mentor_id VARCHAR(36) REFERENCES user(id)")
        print("Added mentor_id to user table.")
    except sqlite3.OperationalError as e:
        print(f"Column mentor_id might already exist: {e}")

    # Create project table
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project (
                id VARCHAR(36) PRIMARY KEY,
                mentor_id VARCHAR(36) NOT NULL REFERENCES user(id) ON DELETE CASCADE,
                title VARCHAR NOT NULL,
                description TEXT,
                whatsapp_link VARCHAR,
                github_link VARCHAR,
                image_url VARCHAR,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_project_id ON project (id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_project_mentor_id ON project (mentor_id)")
        print("Created project table.")
    except Exception as e:
        print(f"Error creating project table: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    migrate()
