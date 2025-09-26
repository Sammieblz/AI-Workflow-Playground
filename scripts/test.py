#!/usr/bin/env python3
"""
Test script for AI Workflow Playground
"""

import os
import sys
import requests
import json
import time
from pathlib import Path

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_email_endpoints():
    """Test email workflow endpoints"""
    print("📧 Testing email endpoints...")
    
    # Test email processing
    try:
        response = requests.post("http://localhost:8000/email/process", timeout=10)
        if response.status_code == 200:
            print("✅ Email processing endpoint working")
        else:
            print(f"⚠️  Email processing endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Email processing test failed: {e}")
    
    # Test email drafting
    try:
        test_email = {
            "action": "draft_reply",
            "email_data": {
                "sender": "test@example.com",
                "subject": "Test Question",
                "body": "This is a test email for the AI workflow system."
            }
        }
        response = requests.post("http://localhost:8000/email/draft", 
                               json=test_email, timeout=10)
        if response.status_code == 200:
            print("✅ Email drafting endpoint working")
        else:
            print(f"⚠️  Email drafting endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Email drafting test failed: {e}")

def test_faq_endpoints():
    """Test FAQ workflow endpoints"""
    print("❓ Testing FAQ endpoints...")
    
    try:
        test_question = {
            "question": "What are your business hours?",
            "context": "Customer asking about availability"
        }
        response = requests.post("http://localhost:8000/faq/answer", 
                               json=test_question, timeout=10)
        if response.status_code == 200:
            print("✅ FAQ endpoint working")
            result = response.json()
            print(f"   Answer: {result.get('answer', 'No answer')[:100]}...")
        else:
            print(f"⚠️  FAQ endpoint returned: {response.status_code}")
    except Exception as e:
        print(f"❌ FAQ test failed: {e}")

def test_call_endpoints():
    """Test call workflow endpoints"""
    print("📞 Testing call endpoints...")
    
    # Note: This would require an actual audio file
    print("⚠️  Call endpoints require audio files - skipping for now")

def test_root_endpoint():
    """Test root endpoint"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working")
            data = response.json()
            print(f"   Service: {data.get('message', 'Unknown')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint test failed: {e}")

def wait_for_service(max_wait=30):
    """Wait for service to be ready"""
    print("⏳ Waiting for service to start...")
    
    for i in range(max_wait):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ Service is ready!")
                return True
        except:
            pass
        
        time.sleep(1)
        print(f"   Waiting... ({i+1}/{max_wait})")
    
    print("❌ Service did not start within timeout")
    return False

def main():
    """Main test function"""
    print("🧪 Testing AI Workflow Playground...")
    print("=" * 50)
    
    # Wait for service to be ready
    if not wait_for_service():
        print("❌ Service not available. Please start the application first.")
        sys.exit(1)
    
    # Run tests
    test_root_endpoint()
    test_health_check()
    test_email_endpoints()
    test_faq_endpoints()
    test_call_endpoints()
    
    print("=" * 50)
    print("✅ Testing completed!")
    print("\nNote: Some tests may show warnings if API keys are not configured.")
    print("Make sure to set up your .env file with proper API keys for full functionality.")

if __name__ == "__main__":
    main()
