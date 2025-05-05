# Workout Plan Generator

FastAPI app that generates personalized workout plans based on goals and mood.

## Configuration

This project supports two AI providers for generating workout plans:

- **Ollama (local, free):** Used for local development and staging.
- **OpenAI (cloud, paid):** Used for production and on the `main` branch in CI/CD.

### How it works

- The provider is selected using the `AI_PROVIDER` environment variable:
  - `AI_PROVIDER=ollama` — Uses your local Ollama server (default for dev/staging).
  - `AI_PROVIDER=openai` — Uses OpenAI's GPT API (used in production and on `main` in CI).
- For OpenAI, you must also set the `OPENAI_API_KEY` environment variable.

### Example usage

**Local development or staging:**
```bash
export AI_PROVIDER=ollama
# (Make sure Ollama is running locally)
```

**Production or main branch in CI/CD:**
```bash
export AI_PROVIDER=openai
export OPENAI_API_KEY=sk-...yourkey...
```

**In CI/CD (GitHub Actions):**
- The workflow is set up to use OpenAI only when running on the `main` branch.
- On other branches, it defaults to Ollama (which will only work if you set up Ollama in the runner).

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