# Interviewer Mock API

A FastAPI-based mock API for interviewer management, designed for deployment on Vercel.

## Features

- **CRUD Operations**: Create, read, update, and delete interviewers
- **Skill-based Filtering**: Find interviewers by specific skills
- **Availability Filtering**: Get only available interviewers
- **RESTful API**: Clean and intuitive endpoints
- **Auto-generated Documentation**: Interactive API docs with Swagger UI
- **CORS Enabled**: Ready for frontend integration

## API Endpoints

### Core Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

### Interviewer Management
- `GET /interviewers` - Get all interviewers
- `GET /interviewers/{id}` - Get specific interviewer
- `POST /interviewers` - Create new interviewer
- `PUT /interviewers/{id}` - Update interviewer
- `DELETE /interviewers/{id}` - Delete interviewer

### Filtering
- `GET /interviewers/skills/{skill}` - Get interviewers by skill
- `GET /interviewers/available` - Get available interviewers only

## Data Model

```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john.doe@example.com",
  "skills": ["Python", "FastAPI", "React"],
  "experience_years": 5,
  "rating": 4.8,
  "available": true
}
```

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
4. Open http://localhost:8000 in your browser

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment on Vercel

### Prerequisites
- Vercel account
- Vercel CLI installed (`npm i -g vercel`)

### Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from project directory**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new one
   - Confirm project settings
   - Deploy

5. **Your API will be available at**:
   ```
   https://your-project-name.vercel.app
   ```

### Alternative: GitHub Integration

1. Push your code to GitHub
2. Connect your GitHub repository to Vercel
3. Vercel will automatically deploy on every push

### Environment Variables

If you need environment variables, add them in the Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add your variables

## Project Structure

```
interviewer-mock-api/
├── api/
│   └── index.py          # Vercel entry point
├── main.py               # Local development server
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
└── README.md            # This file
```

## Testing the API

### Using curl
```bash
# Get all interviewers
curl https://your-app.vercel.app/interviewers

# Get specific interviewer
curl https://your-app.vercel.app/interviewers/1

# Create new interviewer
curl -X POST https://your-app.vercel.app/interviewers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "skills": ["Python", "Django"],
    "experience_years": 3,
    "rating": 4.5,
    "available": true
  }'
```

### Using the Interactive Docs
Visit `https://your-app.vercel.app/docs` to test all endpoints directly in your browser.

## Notes

- The API uses in-memory storage, so data will reset on each deployment
- For production use, consider adding a database
- CORS is enabled for all origins - restrict as needed for production
- The API includes sample data for immediate testing

## Support

For issues or questions, please check the FastAPI documentation or Vercel deployment guides.
