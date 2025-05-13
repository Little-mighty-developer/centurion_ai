# Workout Plan Generator

FastAPI app that generates personalized workout plans based on goals and mood.

## Quick Start

1. Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

2. Run the server:
```bash
python3 -m uvicorn app.main:app --reload
```

3. Access the API at `http://127.0.0.1:8000`

## API

### Endpoint
```
GET /plan?goal=<goal>&mood=<mood>
```

Example:
```
GET /plan?goal=build%20abs&mood=tired
```

Response:
```json
{
    "exercises": ["10 slow crunches", "15-minute walk"],
    "duration": "20 minutes",
    "intensity": "light",
    "notes": "Focus on form and breathing"
}
```

## Testing
```bash
python3 -m pytest tests/ -v
```

## Available Plans
- Build Abs: Light to moderate intensity workouts
- Build Glutes: Light to high intensity workouts
- Default: Gentle stretching and walking for unknown combinations