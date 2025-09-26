#!/usr/bin/env python3
"""
Setup script for AI Workflow Playground
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        "data",
        "data/knowledge_base",
        "data/audio_files",
        "logs",
        "workflows/email_agent",
        "workflows/faq_agent", 
        "workflows/call_agent"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            shutil.copy(".env.example", ".env")
            print("📄 Created .env file from template")
            print("⚠️  Please edit .env file with your API keys and configuration")
        else:
            print("❌ .env.example file not found")
    else:
        print("📄 .env file already exists")

def install_dependencies():
    """Install Python dependencies"""
    if os.path.exists("requirements.txt"):
        return run_command("pip install -r requirements.txt", "Installing Python dependencies")
    else:
        print("❌ requirements.txt not found")
        return False

def setup_docker():
    """Setup Docker environment"""
    if shutil.which("docker"):
        print("🐳 Docker is available")
        return True
    else:
        print("❌ Docker not found. Please install Docker first.")
        return False

def create_sample_data():
    """Create sample data files"""
    
    # Sample FAQ data
    faq_content = """Q: What are your business hours?
A: We are open Monday through Friday from 9 AM to 5 PM.

Q: How can I contact customer support?
A: You can reach us by email at support@yourbusiness.com or call us at (555) 123-4567.

Q: What is your return policy?
A: We offer a 30-day return policy for all products in original condition.

Q: Do you offer technical support?
A: Yes, we provide technical support for all our products. Contact us for assistance.

Q: What payment methods do you accept?
A: We accept all major credit cards, PayPal, and bank transfers.
"""
    
    with open("data/knowledge_base/faq.txt", "w") as f:
        f.write(faq_content)
    
    # Sample product information
    product_content = """Our Products and Services:

1. Business Consulting Services
   - Strategic planning and analysis
   - Process optimization
   - Technology implementation

2. Customer Support Solutions
   - 24/7 support availability
   - Multi-channel support (email, phone, chat)
   - Knowledge base management

3. Automation Tools
   - Workflow automation
   - Email management
   - Call processing and transcription

Pricing:
- Basic Plan: $99/month
- Professional Plan: $199/month
- Enterprise Plan: $399/month
"""
    
    with open("data/knowledge_base/products.txt", "w") as f:
        f.write(product_content)
    
    print("📄 Created sample knowledge base files")

def main():
    """Main setup function"""
    print("🚀 Setting up AI Workflow Playground...")
    print("=" * 50)
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False
    
    # Setup Docker
    if not setup_docker():
        print("⚠️  Docker setup incomplete, but you can continue with local development")
    
    # Create sample data
    create_sample_data()
    
    print("=" * 50)
    print("✅ Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python main.py (for local development)")
    print("3. Or run: docker-compose up (for Docker)")
    print("\nAPI endpoints will be available at:")
    print("- Email: http://localhost:8000/email/")
    print("- FAQ: http://localhost:8000/faq/")
    print("- Call: http://localhost:8000/call/")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
