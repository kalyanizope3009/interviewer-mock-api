from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
from models import SessionInfo, QuestionResponse, Session, Question, UserAnswer
from utils import generate_session_id, get_current_timestamp

logger = logging.getLogger(__name__)

class SessionManager:
    """
    In-memory session management for interview sessions
    """
    
    def __init__(self):
        # In-memory storage for sessions
        self.sessions: Dict[str, Dict[str, Any]] = {}
        # Session timeout (24 hours)
        self.session_timeout = timedelta(hours=24)
        
    def create_session(self, domain: str, interview_type: str, questions: List[QuestionResponse], 
                      adapter_used: str, resume_text: Optional[str] = None, 
                      job_description: Optional[str] = None) -> str:
        """
        Create a new interview session
        
        Args:
            domain: Job domain
            interview_type: Type of interview
            questions: Generated questions
            adapter_used: AI adapter that was used
            
        Returns:
            Session ID
        """
        session_id = generate_session_id()
        
        session_data = {
            "session_id": session_id,
            "domain": domain,
            "interview_type": interview_type,
            "resume_text": resume_text,
            "job_description": job_description,
            "questions": [q.dict() for q in questions],
            "adapter_used": adapter_used,
            "total_questions": len(questions),
            "questions_answered": 0,
            "answers": [],
            "total_score": None,
            "created_at": get_current_timestamp(),
            "status": "active"
        }
        
        self.sessions[session_id] = session_data
        logger.info(f"Created new session {session_id} for {domain} {interview_type} interview")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data by ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data or None if not found
        """
        if session_id not in self.sessions:
            return None
            
        session = self.sessions[session_id]
        
        # Check if session has expired
        created_at = datetime.fromisoformat(session["created_at"])
        if datetime.now() - created_at > self.session_timeout:
            logger.info(f"Session {session_id} has expired, removing")
            del self.sessions[session_id]
            return None
            
        return session
    
    def update_session_answers(self, session_id: str, answers: List[Dict[str, Any]]) -> bool:
        """
        Update session with user answers
        
        Args:
            session_id: Session identifier
            answers: List of user answers
            
        Returns:
            True if successful, False if session not found
        """
        if session_id not in self.sessions:
            logger.warning(f"Attempted to update non-existent session {session_id}")
            return False
            
        session = self.sessions[session_id]
        session["answers"] = answers
        session["questions_answered"] = len(answers)
        
        logger.info(f"Updated session {session_id} with {len(answers)} answers")
        return True
    
    def get_session_info(self, session_id: str) -> Optional[SessionInfo]:
        """
        Get session information as SessionInfo model
        
        Args:
            session_id: Session identifier
            
        Returns:
            SessionInfo object or None if not found
        """
        session = self.get_session(session_id)
        if not session:
            return None
            
        return SessionInfo(
            session_id=session["session_id"],
            domain=session["domain"],
            interview_type=session["interview_type"],
            total_questions=session["total_questions"],
            questions_answered=session["questions_answered"],
            created_at=session["created_at"],
            status=session["status"],
            total_score=float(session["total_score"]) if session["total_score"] else None
        )
    
    def end_session(self, session_id: str) -> bool:
        """
        End a session (mark as completed)
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful, False if session not found
        """
        if session_id not in self.sessions:
            return False
            
        self.sessions[session_id]["status"] = "completed"
        logger.info(f"Ended session {session_id}")
        return True
    
    def cleanup_expired_sessions(self):
        """
        Remove expired sessions from memory
        """
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            created_at = datetime.fromisoformat(session["created_at"])
            if current_time - created_at > self.session_timeout:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
            logger.info(f"Cleaned up expired session {session_id}")
    
    def get_all_sessions(self) -> List[SessionInfo]:
        """
        Get information about all active sessions
        
        Returns:
            List of SessionInfo objects
        """
        self.cleanup_expired_sessions()
        return [self.get_session_info(session_id) for session_id in self.sessions.keys()]

# Global session manager instance
session_manager = SessionManager()
