from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import Optional
import json

from models import (
    GenerateQuestionsRequest, GenerateQuestionsResponse, 
    SubmitAnswersRequest, SubmitAnswersResponse, SessionInfo, ErrorResponse
)
from utils import parse_pdf_to_text, get_adapter_for_interview_type
from session_manager import session_manager
from ai_client import ai_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Mock Interviewer API",
    description="Backend API for AI-powered mock interview system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-mock-interviewer-api"}

@app.post("/gen_questions", response_model=GenerateQuestionsResponse)
async def generate_questions(
    domain: str = Form(...),
    interview_type: str = Form(...),
    resume_file: Optional[UploadFile] = File(None),
    jd_text: Optional[str] = Form(None),
    n: int = Form(8)
):
    """
    Generate interview questions based on user input
    
    Args:
        domain: Job domain (e.g., "Data Scientist", "Software Engineer")
        interview_type: Type of interview (HR, Behavioral, Technical, Coding, All)
        resume_file: Uploaded resume file (PDF or TXT)
        jd_text: Job description text
        n: Number of questions to generate (1-20)
    
    Returns:
        Generated questions with session information
    """
    try:
        logger.info(f"Generating questions for {domain} {interview_type} interview")
        
        # Parse resume if provided
        resume_text = None
        if resume_file:
            if resume_file.content_type == "application/pdf":
                content = await resume_file.read()
                resume_text = parse_pdf_to_text(content)
            elif resume_file.content_type == "text/plain":
                content = await resume_file.read()
                resume_text = content.decode('utf-8')
            else:
                raise HTTPException(status_code=400, detail="Resume file must be PDF or TXT")
        
        # Get the adapter for the interview type
        adapter = get_adapter_for_interview_type(interview_type)
        
        # Generate questions using AI
        questions = ai_client.generate_questions(
            domain=domain,
            interview_type=interview_type,
            resume_text=resume_text,
            jd_text=jd_text,
            n=n
        )
        
        # Create session
        session_id = session_manager.create_session(
            domain=domain,
            interview_type=interview_type,
            questions=questions,
            adapter_used=adapter,
            resume_text=resume_text,
            job_description=jd_text
        )
        
        logger.info(f"Successfully generated {len(questions)} questions for session {session_id}")
        
        return GenerateQuestionsResponse(
            session_id=session_id,
            questions=questions,
            adapter_used=adapter,
            total_questions=len(questions)
        )
        
    except Exception as e:
        logger.error(f"Error generating questions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {str(e)}")

@app.get("/sessions/{session_id}", response_model=SessionInfo)
async def get_session(session_id: str):
    """
    Get session information
    
    Args:
        session_id: Session identifier
        
    Returns:
        Session information
    """
    session_info = session_manager.get_session_info(session_id)
    if not session_info:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session_info

@app.post("/sessions/{session_id}/answers", response_model=SubmitAnswersResponse)
async def submit_answers(session_id: str, request: SubmitAnswersRequest):
    """
    Submit answers for a session
    
    Args:
        session_id: Session identifier
        request: Answers data
        
    Returns:
        Confirmation of answers received
    """
    try:
        # Check if session exists
        session = session_manager.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Update session with answers
        success = session_manager.update_session_answers(session_id, request.answers)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update session")
        
        logger.info(f"Received {len(request.answers)} answers for session {session_id}")
        
        return SubmitAnswersResponse(
            success=True,
            message=f"Successfully received {len(request.answers)} answers",
            answers_received=len(request.answers)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting answers: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to submit answers: {str(e)}")

@app.get("/sessions")
async def list_sessions():
    """
    List all active sessions
    
    Returns:
        List of active sessions
    """
    sessions = session_manager.get_all_sessions()
    return {"sessions": sessions, "total": len(sessions)}

@app.delete("/sessions/{session_id}")
async def end_session(session_id: str):
    """
    End a session
    
    Args:
        session_id: Session identifier
        
    Returns:
        Confirmation of session end
    """
    success = session_manager.end_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session ended successfully"}

# This is important for Vercel
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)