from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.logic_engine import generate_plan, generate_ai_plan
from datetime import date

app = FastAPI(
    title="Workout Plan Generator",
    description="Generate personalized workout plans based on your goals and current mood",
    version="1.0.0"
)

# In-memory storage for check-ins: {user_id: {date: CheckinData}}
checkins = {}

class WorkoutPlanResponse(BaseModel):
    exercises: List[str]
    duration: str
    intensity: str
    notes: Optional[str] = None

class CheckinData(BaseModel):
    date: date
    workout1: bool
    workout2: bool
    water: bool
    reading: bool
    diet: bool
    photo: bool
    notes: Optional[str] = None

class SummaryResponse(BaseModel):
    days_completed: int
    current_streak: int
    last_checkin: Optional[date]
    encouragement: str

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

@app.get("/ai-plan")
def get_ai_workout_plan(goal: str, mood: str):
    """
    Generate a workout plan using OpenAI GPT-3.5 based on goal and mood.
    """
    try:
        plan = generate_ai_plan(goal, mood)
        return {"goal": goal, "mood": mood, "ai_plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/checkin", response_model=SummaryResponse)
def submit_checkin(
    user_id: str = Body(...),
    checkin: CheckinData = Body(...)
):
    """
    Submit a daily 75 Hard check-in for a user.
    """
    user_data = checkins.setdefault(user_id, {})
    user_data[checkin.date] = checkin
    # Calculate streak and days completed
    sorted_days = sorted(user_data.keys())
    streak = 0
    last_day = None
    for d in reversed(sorted_days):
        c = user_data[d]
        if all([c.workout1, c.workout2, c.water, c.reading, c.diet, c.photo]):
            if last_day is None or (last_day - d).days == 1:
                streak += 1
                last_day = d
            else:
                break
        else:
            break
    days_completed = sum(
        1 for c in user_data.values() if all([c.workout1, c.workout2, c.water, c.reading, c.diet, c.photo])
    )
    encouragement = (
        f"Great job! You're on a {streak}-day streak!" if streak > 0 else "Let's get back on track!"
    )
    return SummaryResponse(
        days_completed=days_completed,
        current_streak=streak,
        last_checkin=checkin.date,
        encouragement=encouragement
    )

@app.get("/summary", response_model=SummaryResponse)
def get_summary(user_id: str):
    """
    Get a summary of a user's 75 Hard progress.
    """
    user_data = checkins.get(user_id, {})
    if not user_data:
        return SummaryResponse(
            days_completed=0,
            current_streak=0,
            last_checkin=None,
            encouragement="Let's get started!"
        )
    sorted_days = sorted(user_data.keys())
    streak = 0
    last_day = None
    for d in reversed(sorted_days):
        c = user_data[d]
        if all([c.workout1, c.workout2, c.water, c.reading, c.diet, c.photo]):
            if last_day is None or (last_day - d).days == 1:
                streak += 1
                last_day = d
            else:
                break
        else:
            break
    days_completed = sum(
        1 for c in user_data.values() if all([c.workout1, c.workout2, c.water, c.reading, c.diet, c.photo])
    )
    encouragement = (
        f"Great job! You're on a {streak}-day streak!" if streak > 0 else "Let's get back on track!"
    )
    return SummaryResponse(
        days_completed=days_completed,
        current_streak=streak,
        last_checkin=sorted_days[-1],
        encouragement=encouragement
    )
