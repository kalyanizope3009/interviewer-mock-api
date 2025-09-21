# Interviewer Mock API

A simple FastAPI-based mock API with health check endpoint, designed for deployment on Vercel.

## Features

- **Health Check Endpoint**: Simple monitoring endpoint
- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Vercel Deployment Ready**: Configured for serverless deployment
- **Minimal Dependencies**: Lightweight and fast

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint
  - **Response**: `{"status": "healthy", "service": "interviewer-mock-api"}`

## Local Development

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   python main.py
   ```
4. Test the health endpoint:
   ```bash
   curl http://localhost:8000/health
   ```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment on Vercel
api link: https://interviewer-mock-api.vercel.app/docs


### GitHub Integration

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Vercel will automatically deploy on every push

