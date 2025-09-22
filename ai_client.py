import requests
import logging
from typing import List, Dict, Any, Optional
from models import QuestionResponse
from utils import get_adapter_for_interview_type, create_ai_prompt

logger = logging.getLogger(__name__)

class AIClient:
    """
    Client for interacting with the AI model API
    """
    
    def __init__(self, base_url: str = "https://derivable-agitatedly-ollie.ngrok-free.app"):
        self.base_url = base_url
        self.generate_endpoint = f"{base_url}/generate"
        
    def generate_questions(self, domain: str, interview_type: str, resume_text: Optional[str], 
                          jd_text: Optional[str], n: int = 8) -> List[QuestionResponse]:
        """
        Generate interview questions using the AI model
        
        Args:
            domain: Job domain
            interview_type: Type of interview
            resume_text: Resume content
            jd_text: Job description
            n: Number of questions to generate
            
        Returns:
            List of generated questions
            
        Raises:
            Exception: If AI model call fails
        """
        try:
            # Get the appropriate adapter
            adapter = get_adapter_for_interview_type(interview_type)
            
            # Create the prompt
            prompt = create_ai_prompt(domain, resume_text, jd_text, interview_type, n)
            
            # Prepare the request payload with optimized parameters
            payload = {
                "prompt": prompt,
                "max_new_tokens": 2048,  # Increased for questions + answers
                "temperature": 0.3,  # Lower temperature for more focused, structured output
                "top_p": 0.9,  # Slightly lower for more focused responses
                "top_k": 50,  # Limit vocabulary for better structure
                "repetition_penalty": 1.1,  # Reduce repetition
                "return_full_text": False,
                "adapter": adapter
            }
            
            logger.info(f"Calling AI model with adapter: {adapter}")
            logger.info(f"Prompt length: {len(prompt)} characters")
            
            # Make the API call
            response = requests.post(
                self.generate_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=600  # 10 minute timeout for AI model generation
            )
            
            if response.status_code != 200:
                logger.error(f"AI model returned status {response.status_code}: {response.text}")
                raise Exception(f"AI model API error: {response.status_code}")
            
            # Parse the response
            ai_response = response.json()
            generated_text = ai_response.get("text", "")
            used_adapter = ai_response.get("used_adapter", adapter)
            
            logger.info(f"AI model response length: {len(generated_text)} characters")
            logger.info(f"Used adapter: {used_adapter}")
            
            # Parse the generated text into questions
            questions = self._parse_questions_from_text(generated_text, n, interview_type)
            
            logger.info(f"Successfully generated {len(questions)} questions")
            return questions
            
        except requests.exceptions.Timeout:
            logger.error("AI model request timed out")
            raise Exception("AI model request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to AI model")
            raise Exception("Failed to connect to AI model. Please check if the service is running.")
        except Exception as e:
            logger.error(f"Error calling AI model: {str(e)}")
            raise Exception(f"AI model error: {str(e)}")
    
    def _parse_questions_from_text(self, text: str, expected_count: int, interview_type: str = "Technical") -> List[QuestionResponse]:
        """
        Parse the AI-generated text into Question objects with predicted answers
        
        Args:
            text: Raw text from AI model
            expected_count: Expected number of questions
            interview_type: The type of interview to determine question type
            
        Returns:
            List of Question objects with predicted answers
        """
        import re
        
        # Simple regex to find Q1:, Q2:, etc. patterns
        question_pattern = r'Q(\d+):\s*(.*?)(?=Q\d+:|$)'
        matches = re.findall(question_pattern, text, re.DOTALL)
        
        questions = []
        question_type_map = {
            "HR": "hr",
            "Behavioral": "behavioral", 
            "Technical": "technical",
            "Coding": "coding",
            "All": "mixed"
        }
        question_type = question_type_map.get(interview_type, "interview_question")
        
        for i, (q_num, content) in enumerate(matches):
            content = content.strip()
            
            # Look for corresponding answer (A1:, A2:, etc.)
            answer_pattern = rf'A{q_num}:\s*(.*?)(?=\n|$)'
            answer_match = re.search(answer_pattern, content, re.DOTALL)
            
            if answer_match:
                predicted_answer = answer_match.group(1).strip()
                # Remove answer from question text
                question_text = re.sub(rf'\n?A{q_num}:.*$', '', content, flags=re.DOTALL).strip()
            else:
                question_text = content
                predicted_answer = None
            
            questions.append(QuestionResponse(
                id=f"q_{i + 1}",
                question_text=question_text,
                question_type=question_type,
                predicted_answer=predicted_answer
            ))
        
        # If we didn't get enough questions, create fallbacks
        if len(questions) < expected_count:
            logger.warning(f"Only got {len(questions)} questions, expected {expected_count}")
            for i in range(len(questions), expected_count):
                questions.append(QuestionResponse(
                    id=f"q_{i + 1}",
                    question_text=f"Please provide a detailed answer to this {i + 1}th interview question.",
                    question_type=question_type,
                    predicted_answer="This is a sample question. Please provide a comprehensive answer based on your experience and knowledge."
                ))
        
        return questions[:expected_count]

# Global AI client instance
ai_client = AIClient()
