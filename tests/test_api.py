from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_plan_build_abs_tired():
    response = client.get("/plan?goal=build%20abs&mood=tired")
    assert response.status_code == 200
    data = response.json()
    assert "exercises" in data
    assert "duration" in data
    assert "intensity" in data
    assert "notes" in data
    assert "10 slow crunches" in data["exercises"]
    assert data["duration"] == "20 minutes"
    assert data["intensity"] == "light"

def test_read_plan_build_glutes_energised():
    response = client.get("/plan?goal=build%20glutes&mood=energised")
    assert response.status_code == 200
    data = response.json()
    assert "20 squats" in data["exercises"]
    assert "15 lunges" in data["exercises"]
    assert "10 hip thrusts" in data["exercises"]
    assert data["duration"] == "45 minutes"
    assert data["intensity"] == "high"

def test_read_plan_unknown_combination():
    response = client.get("/plan?goal=unknown&mood=unknown")
    assert response.status_code == 200
    data = response.json()
    assert "gentle stretching" in data["exercises"]
    assert "light walk" in data["exercises"]
    assert data["duration"] == "20 minutes"
    assert data["intensity"] == "light"

def test_read_plan_missing_parameters():
    response = client.get("/plan")
    assert response.status_code == 422  # FastAPI validation error 