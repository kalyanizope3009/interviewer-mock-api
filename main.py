from fastapi import FastAPI

app = FastAPI(
    title="Interviewer Mock API",
    description="A simple mock API with health check",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "interviewer-mock-api"}


# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)