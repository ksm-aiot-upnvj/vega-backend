import sys
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.get("/api/v1/categories/")
print(response.status_code)
print(response.text)

response2 = client.get("/api/v1/courses/")
print(response2.status_code)
print(response2.text)
