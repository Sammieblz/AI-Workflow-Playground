#!/usr/bin/env python3
"""
Deployment script for AI Workflow Playground
"""

import os
import sys
import subprocess
import argparse
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

def deploy_local():
    """Deploy locally"""
    print("🏠 Deploying locally...")
    
    # Check if .env exists
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please run setup.py first.")
        return False
    
    # Start the application
    return run_command("python main.py", "Starting local application")

def deploy_docker():
    """Deploy using Docker"""
    print("🐳 Deploying with Docker...")
    
    # Check if docker-compose.yml exists
    if not os.path.exists("docker/docker-compose.yml"):
        print("❌ docker-compose.yml not found")
        return False
    
    # Build and start containers
    commands = [
        "docker-compose -f docker/docker-compose.yml build",
        "docker-compose -f docker/docker-compose.yml up -d"
    ]
    
    for command in commands:
        if not run_command(command, f"Running: {command}"):
            return False
    
    print("✅ Docker deployment completed")
    print("🌐 Application should be running at http://localhost:8000")
    return True

def deploy_vps():
    """Deploy to VPS (placeholder)"""
    print("☁️  VPS deployment not implemented yet")
    print("This would typically involve:")
    print("- SSH to VPS")
    print("- Clone repository")
    print("- Setup environment")
    print("- Start services")
    return True

def deploy_cloud():
    """Deploy to cloud (placeholder)"""
    print("☁️  Cloud deployment not implemented yet")
    print("This would typically involve:")
    print("- Container registry")
    print("- Kubernetes cluster")
    print("- Load balancer setup")
    print("- Auto-scaling configuration")
    return True

def main():
    """Main deployment function"""
    parser = argparse.ArgumentParser(description="Deploy AI Workflow Playground")
    parser.add_argument("target", choices=["local", "docker", "vps", "cloud"], 
                       help="Deployment target")
    
    args = parser.parse_args()
    
    print(f"🚀 Deploying to {args.target}...")
    print("=" * 50)
    
    if args.target == "local":
        success = deploy_local()
    elif args.target == "docker":
        success = deploy_docker()
    elif args.target == "vps":
        success = deploy_vps()
    elif args.target == "cloud":
        success = deploy_cloud()
    else:
        print("❌ Invalid deployment target")
        success = False
    
    if success:
        print("✅ Deployment completed successfully!")
    else:
        print("❌ Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
