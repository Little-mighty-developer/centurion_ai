from typing import Dict, List, Optional
import os
import openai
import requests

class WorkoutPlan:
    def __init__(self, exercises: List[str], duration: str, intensity: str, notes: Optional[str] = None):
        self.exercises = exercises
        self.duration = duration
        self.intensity = intensity
        self.notes = notes

    def to_dict(self) -> Dict:
        return {
            "exercises": self.exercises,
            "duration": self.duration,
            "intensity": self.intensity,
            "notes": self.notes
        }

# Predefined workout plans
WORKOUT_PLANS = {
    "build abs": {
        "tired": WorkoutPlan(
            exercises=["10 slow crunches", "15-minute walk"],
            duration="20 minutes",
            intensity="light",
            notes="Focus on form and breathing"
        ),
        "energised": WorkoutPlan(
            exercises=["30 crunches", "20 leg raises", "2-minute plank"],
            duration="30 minutes",
            intensity="moderate",
            notes="Push yourself but maintain good form"
        )
    },
    "build glutes": {
        "tired": WorkoutPlan(
            exercises=["10 glute bridges", "stretching"],
            duration="15 minutes",
            intensity="light",
            notes="Focus on mind-muscle connection"
        ),
        "energised": WorkoutPlan(
            exercises=["20 squats", "15 lunges", "10 hip thrusts"],
            duration="45 minutes",
            intensity="high",
            notes="Complete 3 rounds with 1-minute rest between"
        )
    }
}

def generate_plan(goal: str, mood: str) -> Dict:
    """
    Generate a workout plan based on goal and mood.
    
    Args:
        goal (str): The fitness goal (e.g., "build abs", "build glutes")
        mood (str): The current mood (e.g., "tired", "energised")
        
    Returns:
        Dict: A structured workout plan
    """
    # Normalize inputs
    goal = goal.lower().strip()
    mood = mood.lower().strip()
    
    # Check if we have a predefined plan
    if goal in WORKOUT_PLANS and mood in WORKOUT_PLANS[goal]:
        return WORKOUT_PLANS[goal][mood].to_dict()
    
    # Default plan for unknown combinations
    return WorkoutPlan(
        exercises=["gentle stretching", "light walk"],
        duration="20 minutes",
        intensity="light",
        notes="Listen to your body and adjust intensity as needed"
    ).to_dict()

def generate_ollama_plan(goal: str, mood: str, model: str = "llama3") -> str:
    """
    Generate a workout plan using Ollama's local LLM API.
    """
    prompt = (
        f"You are a helpful fitness assistant. "
        f"Given the goal: '{goal}' and the mood: '{mood}', "
        f"generate a concise, actionable workout plan. "
        f"Be specific, safe, and motivating."
    )
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"Ollama API error: {e}")

def generate_ai_plan(goal: str, mood: str) -> str:
    """
    Generate a workout plan using the selected AI provider (OpenAI or Ollama).
    """
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    if provider == "ollama":
        return generate_ollama_plan(goal, mood)
    else:
        # Default to OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY environment variable not set.")
        openai.api_key = api_key

        prompt = (
            f"You are a helpful fitness assistant. "
            f"Given the goal: '{goal}' and the mood: '{mood}', "
            f"generate a concise, actionable workout plan. "
            f"Be specific, safe, and motivating."
        )
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
