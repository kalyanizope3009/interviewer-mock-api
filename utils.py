import PyPDF2
import io
import logging
from typing import Optional
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_pdf_to_text(pdf_content: bytes) -> str:
    """
    Parse PDF content to text using PyPDF2
    
    Args:
        pdf_content: PDF file content as bytes
        
    Returns:
        Extracted text from PDF
        
    Raises:
        Exception: If PDF parsing fails
    """
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
        text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
            
        # Clean up the text
        text = text.strip()
        if not text:
            raise ValueError("No text could be extracted from the PDF")
            
        logger.info(f"Successfully extracted {len(text)} characters from PDF")
        return text
        
    except Exception as e:
        logger.error(f"Failed to parse PDF: {str(e)}")
        raise Exception(f"PDF parsing failed: {str(e)}")

def generate_session_id() -> str:
    """Generate a unique session ID"""
    return str(uuid.uuid4())

def get_current_timestamp() -> str:
    """Get current timestamp as ISO string"""
    return datetime.now().isoformat()

# Adapter mapping for interview types
INTERVIEW_TYPE_TO_ADAPTER = {
    "HR": "finetuned_Hr",
    "Behavioral": "finetuned_Behavioral", 
    "Technical": "finetuned_Technical",
    "Coding": "finetuned_Dsa",
    "All": "finetuned_Sql"
}

def get_adapter_for_interview_type(interview_type: str) -> str:
    """
    Get the appropriate adapter name for the interview type
    
    Args:
        interview_type: The type of interview (HR, Behavioral, etc.)
        
    Returns:
        The adapter name to use with the AI model
    """
    return INTERVIEW_TYPE_TO_ADAPTER.get(interview_type, "finetuned_Technical")

def create_ai_prompt(domain: str, resume_text: Optional[str], jd_text: Optional[str], 
                    interview_type: str, n: int) -> str:
    """
    Create a prompt for the AI model to generate interview questions
    
    Args:
        domain: Job domain
        resume_text: Resume content
        jd_text: Job description
        interview_type: Type of interview
        n: Number of questions
        
    Returns:
        Formatted prompt for the AI model
    """
    # Optimized prompt for better AI results
    context_parts = [
        f"You are a senior {domain} interviewer. Generate {n} {interview_type.lower()} questions.",
        "",
        "REQUIREMENTS:",
        "- Each question must be practical and role-specific",
        "- Include mix of difficulty levels (basic, intermediate, advanced)",
        "- Focus on real-world scenarios and problem-solving",
        "- Questions should test both technical knowledge and practical skills"
    ]
    
    # Add context if available
    if resume_text:
        resume_summary = resume_text[:300].replace('\n', ' ').strip()
        context_parts.extend([
            "",
            f"CANDIDATE: {resume_summary}",
            "Adjust difficulty based on their experience level."
        ])
    
    if jd_text:
        jd_summary = jd_text[:300].replace('\n', ' ').strip()
        context_parts.extend([
            "",
            f"ROLE: {jd_summary}",
            "Focus on the key skills and technologies mentioned."
        ])
    
    context_parts.extend([
        "",
        "CRITICAL FORMATTING RULES:",
        "1. Start each question with exactly 'Q1:', 'Q2:', etc.",
        "2. Start each answer with exactly 'A1:', 'A2:', etc.",
        "3. Keep questions concise but specific",
        "4. Answers should include key points and approach",
        "5. Use line breaks between Q and A pairs",
        "",
        "EXAMPLE:",
        "Q1: How would you optimize a slow database query?",
        "A1: Key points: Identify bottlenecks, use indexes, optimize joins, consider caching. Approach: Analyze execution plan, add appropriate indexes, rewrite query if needed.",
        "",
        f"Generate {n} questions for {domain}:"
    ])
    
    return "\n".join(context_parts)
