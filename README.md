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
├── test_api.py          # Test script
└── README.md            # This file
```

## Testing the API

### Using curl
```bash
# Test health endpoint
curl https://your-app.vercel.app/health

# Expected response:
# {"status": "healthy", "service": "interviewer-mock-api"}
```

### Using the Interactive Docs
Visit `https://your-app.vercel.app/docs` to test the endpoint directly in your browser.

## Troubleshooting

### Common Issues

1. **500 Error on Vercel**: 
   - Check Vercel logs: `vercel logs <deployment-url>`
   - Ensure `api/index.py` exists and has the correct handler export
   - Verify `vercel.json` configuration

2. **Import Errors**:
   - Make sure all dependencies are in `requirements.txt`
   - Check Python version compatibility

3. **Local Development Issues**:
   - Ensure Python 3.8+ is installed
   - Install dependencies: `pip install -r requirements.txt`
   - Check if port 8000 is available

### Debugging Steps
1. Test locally first: `python main.py`
2. Check Vercel deployment logs
3. Verify file structure matches Vercel requirements
4. Test with simple curl requests

## Notes

- This is a minimal API with just a health check endpoint
- Perfect for monitoring and basic connectivity testing
- Ready for expansion with additional endpoints as needed

## Support

For issues or questions, please check the FastAPI documentation or Vercel deployment guides.
