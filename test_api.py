#!/usr/bin/env python3
"""
Simple test script for the AI Mock Interviewer API
"""

import requests
import json
from typing import Dict, Any

# Test configuration
API_BASE_URL = "http://localhost:8000"  # Change this to your deployed URL

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

def test_generate_questions():
    """Test question generation endpoint"""
    print("\n🔍 Testing question generation...")
    
    # Test data
    test_data = {
        "domain": "Data Scientist",
        "interview_type": "Technical",
        "jd_text": "Looking for a data scientist with experience in machine learning, Python, and SQL.",
        "n": 3
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/gen_questions",
            data=test_data,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Question generation passed")
            print(f"   Session ID: {result['session_id']}")
            print(f"   Adapter used: {result['adapter_used']}")
            print(f"   Questions generated: {result['total_questions']}")
            
            # Print first question as example
            if result['questions']:
                print(f"   Sample question: {result['questions'][0]['question_text'][:100]}...")
            
            return result['session_id']
        else:
            print(f"❌ Question generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Question generation error: {e}")
        return None

def test_session_management(session_id: str):
    """Test session management endpoints"""
    if not session_id:
        print("\n⏭️  Skipping session tests (no session ID)")
        return
    
    print(f"\n🔍 Testing session management for {session_id}...")
    
    # Test get session
    try:
        response = requests.get(f"{API_BASE_URL}/sessions/{session_id}")
        if response.status_code == 200:
            session_info = response.json()
            print("✅ Get session passed")
            print(f"   Domain: {session_info['domain']}")
            print(f"   Interview type: {session_info['interview_type']}")
            print(f"   Questions answered: {session_info['questions_answered']}")
        else:
            print(f"❌ Get session failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Get session error: {e}")
    
    # Test submit answers
    try:
        test_answers = [
            {"question_id": "q_1", "answer_text": "This is a test answer for question 1."},
            {"question_id": "q_2", "answer_text": "This is a test answer for question 2."}
        ]
        
        response = requests.post(
            f"{API_BASE_URL}/sessions/{session_id}/answers",
            json={"answers": test_answers}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Submit answers passed")
            print(f"   Answers received: {result['answers_received']}")
        else:
            print(f"❌ Submit answers failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Submit answers error: {e}")

def test_list_sessions():
    """Test listing all sessions"""
    print("\n🔍 Testing list sessions...")
    try:
        response = requests.get(f"{API_BASE_URL}/sessions")
        if response.status_code == 200:
            result = response.json()
            print("✅ List sessions passed")
            print(f"   Total sessions: {result['total']}")
        else:
            print(f"❌ List sessions failed: {response.status_code}")
    except Exception as e:
        print(f"❌ List sessions error: {e}")

def main():
    """Run all tests"""
    print("🚀 Starting AI Mock Interviewer API Tests")
    print("=" * 50)
    
    # Run tests
    test_health_check()
    session_id = test_generate_questions()
    test_session_management(session_id)
    test_list_sessions()
    
    print("\n" + "=" * 50)
    print("🏁 Tests completed!")
    
    if session_id:
        print(f"\n💡 You can test the session manually:")
        print(f"   GET {API_BASE_URL}/sessions/{session_id}")
        print(f"   DELETE {API_BASE_URL}/sessions/{session_id}")

if __name__ == "__main__":
    main()