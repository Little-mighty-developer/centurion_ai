from typing import Dict, List, Optional

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
