#!/usr/bin/env python3
"""
Advanced deployment script for AI Workflow Playground with integrations
"""

import os
import sys
import subprocess
import argparse
import json
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

def check_requirements():
    """Check if all required tools are installed"""
    requirements = {
        "python": "python --version",
        "docker": "docker --version",
        "node": "node --version"
    }
    
    missing = []
    for tool, command in requirements.items():
        if not run_command(command, f"Checking {tool}"):
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing requirements: {', '.join(missing)}")
        print("Please install the missing tools before continuing.")
        return False
    
    return True

def setup_environment():
    """Setup environment variables for integrations"""
    env_vars = {
        "ELEVENLABS_API_KEY": "your_elevenlabs_api_key_here",
        "ELEVENLABS_VOICE_ID": "21m00Tcm4TlvDq8ikWAM",
        "N8N_BASIC_AUTH_ACTIVE": "true",
        "N8N_BASIC_AUTH_USER": "admin",
        "N8N_BASIC_AUTH_PASSWORD": "password"
    }
    
    print("🔧 Setting up environment variables...")
    
    # Read existing .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
    else:
        content = ""
    
    # Add missing environment variables
    for key, value in env_vars.items():
        if key not in content:
            content += f"\n# Enhanced integrations\n{key}={value}\n"
    
    # Write updated .env file
    with open(env_file, "w") as f:
        f.write(content)
    
    print("✅ Environment variables configured")
    return True

def install_dependencies():
    """Install Python dependencies"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def setup_n8n():
    """Setup n8n with Docker"""
    print("🐳 Setting up n8n...")
    
    # Create n8n data directory
    n8n_dir = Path("n8n-data")
    n8n_dir.mkdir(exist_ok=True)
    
    # Create n8n docker-compose file
    n8n_compose = """
version: '3.8'

services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - ./n8n-data:/home/node/.n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
      - WEBHOOK_URL=http://localhost:5678/
    restart: unless-stopped
"""
    
    with open("n8n-docker-compose.yml", "w") as f:
        f.write(n8n_compose)
    
    print("✅ n8n configuration created")
    return True

def import_n8n_workflows():
    """Import n8n workflows"""
    print("📋 Importing n8n workflows...")
    
    # Create workflows directory in n8n data
    workflows_dir = Path("n8n-data/workflows")
    workflows_dir.mkdir(exist_ok=True)
    
    # Copy workflow files
    workflow_files = [
        "integrations/n8n_workflows/email_automation.json",
        "integrations/n8n_workflows/voice_automation.json"
    ]
    
    for workflow_file in workflow_files:
        if Path(workflow_file).exists():
            import shutil
            shutil.copy(workflow_file, workflows_dir)
            print(f"✅ Imported {workflow_file}")
    
    return True

def test_integrations():
    """Test all integrations"""
    print("🧪 Testing integrations...")
    
    # Test ElevenLabs
    if os.getenv("ELEVENLABS_API_KEY"):
        print("✅ ElevenLabs API key configured")
    else:
        print("⚠️  ElevenLabs API key not configured")
    
    # Test OpenAI
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key configured")
    else:
        print("⚠️  OpenAI API key not configured")
    
    return True

def deploy_local():
    """Deploy locally with all integrations"""
    print("🏠 Deploying locally with integrations...")
    
    if not check_requirements():
        return False
    
    if not setup_environment():
        return False
    
    if not install_dependencies():
        return False
    
    if not setup_n8n():
        return False
    
    if not import_n8n_workflows():
        return False
    
    if not test_integrations():
        return False
    
    print("✅ Local deployment with integrations completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Start the main application: python main.py")
    print("3. Start n8n: docker-compose -f n8n-docker-compose.yml up")
    print("4. Access n8n at http://localhost:5678")
    print("5. Test integrations at http://localhost:8000/enhanced/status")
    
    return True

def deploy_docker():
    """Deploy with Docker including integrations"""
    print("🐳 Deploying with Docker and integrations...")
    
    # Create enhanced docker-compose file
    enhanced_compose = """
version: '3.8'

services:
  ai-workflows:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    env_file:
      - ../.env
    volumes:
      - ../workflows:/app/workflows
      - ../data:/app/data
      - ../logs:/app/logs
    restart: unless-stopped
    depends_on:
      - n8n

  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=password
      - WEBHOOK_URL=http://localhost:5678/
    restart: unless-stopped

volumes:
  n8n_data:
"""
    
    with open("docker-compose-enhanced.yml", "w") as f:
        f.write(enhanced_compose)
    
    # Deploy with enhanced compose
    commands = [
        "docker-compose -f docker-compose-enhanced.yml build",
        "docker-compose -f docker-compose-enhanced.yml up -d"
    ]
    
    for command in commands:
        if not run_command(command, f"Running: {command}"):
            return False
    
    print("✅ Docker deployment with integrations completed!")
    print("🌐 AI Workflows: http://localhost:8000")
    print("🌐 n8n Interface: http://localhost:5678")
    
    return True

def create_startup_script():
    """Create startup script for all services"""
    startup_script = """#!/bin/bash
# AI Workflow Playground Startup Script

echo "🚀 Starting AI Workflow Playground with integrations..."

# Start main application
echo "Starting AI Workflow API..."
python main.py &
API_PID=$!

# Start n8n
echo "Starting n8n..."
docker-compose -f n8n-docker-compose.yml up -d

# Wait for services to start
echo "Waiting for services to start..."
sleep 10

# Check if services are running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ AI Workflow API is running"
else
    echo "❌ AI Workflow API failed to start"
fi

if curl -f http://localhost:5678 > /dev/null 2>&1; then
    echo "✅ n8n is running"
else
    echo "❌ n8n failed to start"
fi

echo "🎉 All services started!"
echo "AI Workflows: http://localhost:8000"
echo "n8n Interface: http://localhost:5678"
echo "Enhanced API: http://localhost:8000/enhanced/status"

# Keep script running
wait $API_PID
"""
    
    with open("start_advanced.sh", "w") as f:
        f.write(startup_script)
    
    # Make executable
    os.chmod("start_advanced.sh", 0o755)
    
    print("✅ Startup script created: start_advanced.sh")
    return True

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy AI Workflow Playground with integrations")
    parser.add_argument("target", choices=["local", "docker", "setup"], 
                       help="Deployment target")
    
    args = parser.parse_args()
    
    print(f"🚀 Deploying AI Workflow Playground with integrations to {args.target}...")
    print("=" * 60)
    
    if args.target == "setup":
        success = (
            check_requirements() and
            setup_environment() and
            install_dependencies() and
            setup_n8n() and
            import_n8n_workflows() and
            create_startup_script()
        )
    elif args.target == "local":
        success = deploy_local()
    elif args.target == "docker":
        success = deploy_docker()
    else:
        print("❌ Invalid deployment target")
        success = False
    
    if success:
        print("✅ Advanced deployment completed successfully!")
        print("\n🔗 Integration URLs:")
        print("- AI Workflows: http://localhost:8000")
        print("- n8n Interface: http://localhost:5678")
        print("- Enhanced API: http://localhost:8000/enhanced/status")
        print("\n📚 Documentation: integrations/setup_guide.md")
    else:
        print("❌ Advanced deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
