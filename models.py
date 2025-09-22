from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from decimal import Decimal

class InterviewType(str, Enum):
    HR = "HR"
    BEHAVIORAL = "Behavioral"
    TECHNICAL = "Technical"
    CODING = "Coding"
    ALL = "All"

# Database Models (matching schema.sql)

class Session(BaseModel):
    """Session model matching the sessions table"""
    id: str = Field(..., description="Session UUID")
    domain: str = Field(..., max_length=100, description="Job domain")
    interview_type: InterviewType = Field(..., description="Type of interview")
    resume_text: Optional[str] = Field(None, description="Parsed resume content")
    job_description: Optional[str] = Field(None, description="Job description text")
    total_score: Optional[Decimal] = Field(None, ge=0, le=10, description="Overall session score (0-10)")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation timestamp")

class Question(BaseModel):
    """Question model matching the questions table"""
    id: str = Field(..., description="Question UUID")
    session_id: str = Field(..., description="Associated session ID")
    question_text: str = Field(..., description="The interview question")
    predicted_answer: Optional[str] = Field(None, description="Ideal/expected answer")
    question_type: Optional[str] = Field(None, max_length=50, description="Question category")
    created_at: datetime = Field(default_factory=datetime.now, description="Question creation timestamp")

class UserAnswer(BaseModel):
    """User answer model matching the user_answers table"""
    id: str = Field(..., description="Answer UUID")
    session_id: str = Field(..., description="Associated session ID")
    question_id: str = Field(..., description="Associated question ID")
    answer_text: str = Field(..., description="User's answer text")
    time_spent_seconds: Optional[int] = Field(None, description="Time taken to answer")

class Evaluation(BaseModel):
    """Evaluation model matching the evaluations table"""
    id: str = Field(..., description="Evaluation UUID")
    session_id: str = Field(..., description="Associated session ID")
    total_score: Decimal = Field(..., ge=0, le=10, description="Overall session score (0-10)")
    overall_feedback: Optional[str] = Field(None, description="General feedback for the session")
    created_at: datetime = Field(default_factory=datetime.now, description="Evaluation creation timestamp")

# API Request/Response Models

class GenerateQuestionsRequest(BaseModel):
    domain: str = Field(..., description="Job domain (e.g., 'Data Scientist', 'Software Engineer')")
    interview_type: InterviewType = Field(..., description="Type of interview")
    resume_text: Optional[str] = Field(None, description="Resume content as text")
    jd_text: Optional[str] = Field(None, description="Job description text")
    n: int = Field(8, ge=1, le=20, description="Number of questions to generate")

class QuestionResponse(BaseModel):
    """Question response model for API"""
    id: str
    question_text: str
    question_type: Optional[str] = None
    predicted_answer: Optional[str] = None

class GenerateQuestionsResponse(BaseModel):
    session_id: str
    questions: List[QuestionResponse]
    adapter_used: str
    total_questions: int

class SubmitAnswersRequest(BaseModel):
    answers: List[Dict[str, Any]] = Field(..., description="List of answers with question_id, answer_text, and optional time_spent_seconds")

class SubmitAnswersResponse(BaseModel):
    success: bool
    message: str
    answers_received: int

class SessionInfo(BaseModel):
    """Session info for API responses"""
    session_id: str
    domain: str
    interview_type: str
    total_questions: int
    questions_answered: int
    created_at: str
    status: str
    total_score: Optional[float] = None

class EvaluationRequest(BaseModel):
    """Request model for creating evaluations"""
    total_score: Decimal = Field(..., ge=0, le=10, description="Overall session score (0-10)")
    overall_feedback: Optional[str] = Field(None, description="General feedback for the session")

class EvaluationResponse(BaseModel):
    """Evaluation response model"""
    id: str
    session_id: str
    total_score: float
    overall_feedback: Optional[str]
    created_at: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    session_id: Optional[str] = None
