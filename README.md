# AI Mock Interviewer API

Backend API for the AI-powered mock interview system. This API generates personalized interview questions using fine-tuned Mistral 7B models with LoRA adapters.

## Features

- **PDF Resume Parsing**: Converts PDF resumes to text for personalized questions
- **AI Integration**: Calls your fine-tuned Mistral 7B model with appropriate adapters
- **Session Management**: Tracks interview sessions with unique IDs
- **Question Generation**: Creates tailored questions based on domain, resume, and job description
- **Answer Collection**: Stores user responses for evaluation

## Database Schema

The API is designed to work with the following database tables:

- `sessions`: Stores interview session metadata
- `questions`: Stores generated questions with predicted answers
- `user_answers`: Stores user responses to questions
- `evaluations`: Stores session evaluation results

## API Endpoints

### Core Endpoints

- `POST /gen_questions` - Generate interview questions
- `GET /sessions/{session_id}` - Get session information
- `POST /sessions/{session_id}/answers` - Submit user answers
- `GET /sessions` - List all active sessions
- `DELETE /sessions/{session_id}` - End a session

### Health Check

- `GET /health` - API health status

## Adapter Mapping

The API maps interview types to AI model adapters:

- `HR` → `finetuned_Hr`
- `Behavioral` → `finetuned_Behavioral`
- `Technical` → `finetuned_Technical`
- `Coding` → `finetuned_Dsa`
- `All` → `finetuned_Sql`

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
```bash
python main.py
```

## Configuration

Update the AI model URL in `ai_client.py`:
```python
base_url = "https://your-ngrok-url.ngrok-free.app"
```

## Testing

Run the test script to verify API functionality:
```bash
python test_api.py
```

## Deployment

The API is configured for Vercel deployment with `vercel.json`.

## Models

The API uses Pydantic models that match the database schema:

- `Session`: Session metadata
- `Question`: Interview questions
- `UserAnswer`: User responses
- `Evaluation`: Session evaluations

## Error Handling

Comprehensive error handling with proper HTTP status codes and detailed error messages.

## Logging

Structured logging for debugging and monitoring API operations.