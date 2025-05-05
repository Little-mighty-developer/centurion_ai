# tests/test_staging.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_plan_endpoint_staging():
    response = client.get("/plan?goal=build%20abs&mood=tired")
    assert response.status_code == 200
    data = response.json()
    assert "exercises" in data
    assert "duration" in data
    assert "intensity" in data