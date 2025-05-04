from app.logic_engine import generate_plan

def test_generate_plan_build_abs_tired():
    plan = generate_plan("build abs", "tired")
    assert plan["exercises"] == ["10 slow crunches", "15-minute walk"]
    assert plan["duration"] == "20 minutes"
    assert plan["intensity"] == "light"
    assert "form and breathing" in plan["notes"].lower()

def test_generate_plan_build_abs_energised():
    plan = generate_plan("build abs", "energised")
    assert "30 crunches" in plan["exercises"]
    assert "20 leg raises" in plan["exercises"]
    assert "2-minute plank" in plan["exercises"]
    assert plan["duration"] == "30 minutes"
    assert plan["intensity"] == "moderate"

def test_generate_plan_build_glutes_tired():
    plan = generate_plan("build glutes", "tired")
    assert "10 glute bridges" in plan["exercises"]
    assert "stretching" in plan["exercises"]
    assert plan["duration"] == "15 minutes"
    assert plan["intensity"] == "light"

def test_generate_plan_build_glutes_energised():
    plan = generate_plan("build glutes", "energised")
    assert "20 squats" in plan["exercises"]
    assert "15 lunges" in plan["exercises"]
    assert "10 hip thrusts" in plan["exercises"]
    assert plan["duration"] == "45 minutes"
    assert plan["intensity"] == "high"

def test_generate_plan_unknown_combination():
    plan = generate_plan("unknown goal", "unknown mood")
    assert "gentle stretching" in plan["exercises"]
    assert "light walk" in plan["exercises"]
    assert plan["duration"] == "20 minutes"
    assert plan["intensity"] == "light"
    assert "listen to your body" in plan["notes"].lower() 