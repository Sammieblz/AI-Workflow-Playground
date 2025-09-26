"""
AI Workflow Playground - Main Application
FastAPI-based server for running AI agent workflows
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import workflow agents
from workflows.email_agent.email_processor import EmailProcessor
from workflows.faq_agent.faq_processor import FAQProcessor
from workflows.call_agent.call_processor import CallProcessor

# Import enhanced integrations
from integrations.enhanced_api import router as enhanced_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global workflow processors
email_processor = None
faq_processor = None
call_processor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize workflow processors on startup"""
    global email_processor, faq_processor, call_processor
    
    logger.info("Initializing AI Workflow Playground...")
    
    try:
        # Initialize processors
        email_processor = EmailProcessor()
        faq_processor = FAQProcessor()
        call_processor = CallProcessor()
        
        logger.info("All workflow processors initialized successfully")
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize processors: {e}")
        raise
    finally:
        logger.info("Shutting down AI Workflow Playground...")

# Create FastAPI app
app = FastAPI(
    title="AI Workflow Playground",
    description="Modular AI agents for business automation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include enhanced integrations router
app.include_router(enhanced_router)

# Pydantic models for API
class EmailRequest(BaseModel):
    action: str  # "process", "draft_reply", "classify"
    email_data: dict

class FAQRequest(BaseModel):
    question: str
    context: str = ""

class CallRequest(BaseModel):
    audio_file_path: str
    action: str = "transcribe"  # "transcribe", "summarize", "both"

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Workflow Playground"}

# Email workflow endpoints
@app.post("/email/process")
async def process_emails():
    """Process new emails in the inbox"""
    if not email_processor:
        raise HTTPException(status_code=500, detail="Email processor not initialized")
    
    try:
        result = await email_processor.process_emails()
        return {"status": "success", "processed": result["count"], "emails": result["emails"]}
    except Exception as e:
        logger.error(f"Email processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/email/draft")
async def draft_email_reply(request: EmailRequest):
    """Draft a reply to an email"""
    if not email_processor:
        raise HTTPException(status_code=500, detail="Email processor not initialized")
    
    try:
        reply = await email_processor.draft_reply(request.email_data)
        return {"status": "success", "draft_reply": reply}
    except Exception as e:
        logger.error(f"Email drafting error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# FAQ workflow endpoints
@app.post("/faq/answer")
async def answer_question(request: FAQRequest):
    """Answer a customer question using FAQ knowledge base"""
    if not faq_processor:
        raise HTTPException(status_code=500, detail="FAQ processor not initialized")
    
    try:
        answer = await faq_processor.answer_question(request.question, request.context)
        return {"status": "success", "answer": answer}
    except Exception as e:
        logger.error(f"FAQ processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Call workflow endpoints
@app.post("/call/transcribe")
async def transcribe_call(request: CallRequest):
    """Transcribe an audio file"""
    if not call_processor:
        raise HTTPException(status_code=500, detail="Call processor not initialized")
    
    try:
        result = await call_processor.transcribe_audio(request.audio_file_path)
        return {"status": "success", "transcription": result}
    except Exception as e:
        logger.error(f"Call transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/call/summarize")
async def summarize_call(request: CallRequest):
    """Summarize a call transcription"""
    if not call_processor:
        raise HTTPException(status_code=500, detail="Call processor not initialized")
    
    try:
        summary = await call_processor.summarize_call(request.audio_file_path)
        return {"status": "success", "summary": summary}
    except Exception as e:
        logger.error(f"Call summarization error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Workflow Playground",
        "version": "1.0.0",
        "endpoints": {
            "email": ["/email/process", "/email/draft"],
            "faq": ["/faq/answer"],
            "call": ["/call/transcribe", "/call/summarize"]
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )
