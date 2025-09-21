#!/usr/bin/env python3
"""
Simple test script for the Interviewer Mock API
Run this after starting the server to test the health endpoint
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, expected_status=200):
    """Test an API endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url)
        
        print(f"{method} {endpoint} - Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ PASS")
            if response.content:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print("❌ FAIL")
            print(f"Expected: {expected_status}, Got: {response.status_code}")
        
        print("-" * 50)
        return response
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed - Is the server running on {BASE_URL}?")
        return None

def main():
    print("🧪 Testing Interviewer Mock API")
    print("=" * 50)
    
    # Test health endpoint
    test_endpoint("GET", "/health")
    
    print("🎉 Testing completed!")

if __name__ == "__main__":
    main()
