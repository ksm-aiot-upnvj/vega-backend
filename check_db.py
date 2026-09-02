import json
import urllib.request

req = urllib.request.Request("http://127.0.0.1:8000/api/v1/enrollments/me")
req.add_header("Authorization", "Bearer MOCK") # Assuming no auth for dev or we can use a real token
# Wait, I don't have a token. Let's just query the DB directly to see what data is stored in Course table and Enrollment table.

import sqlite3
conn = sqlite3.connect("D:\\Kuliah\\UKM or KSM\\AIOT\\Website\\Vega\\vega-backend\\vega.db")
cursor = conn.cursor()
cursor.execute("SELECT id, course_id FROM enrollment LIMIT 1")
enrollment = cursor.fetchone()
print(f"Enrollment: {enrollment}")
cursor.execute("SELECT id, title FROM course LIMIT 1")
course = cursor.fetchone()
print(f"Course: {course}")
