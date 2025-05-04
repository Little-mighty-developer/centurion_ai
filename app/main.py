from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.logic_engine import generate_plan

app = FastAPI(
    title="Workout Plan Generator",
    description="Generate personalized workout plans based on your goals and current mood",
    version="1.0.0"
)

class WorkoutPlanResponse(BaseModel):
    exercises: List[str]
    duration: str
    intensity: str
    notes: Optional[str] = None

@app.get("/plan", response_model=WorkoutPlanResponse)
def get_workout_plan(goal: str, mood: str):
    """
    Generate a personalized workout plan based on goal and mood.
    
    Args:
        goal (str): The fitness goal (e.g., "build abs", "build glutes")
        mood (str): The current mood (e.g., "tired", "energised")
        
    Returns:
        WorkoutPlanResponse: A structured workout plan containing exercises, duration, intensity, and notes
    """
    try:
        plan = generate_plan(goal, mood)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
